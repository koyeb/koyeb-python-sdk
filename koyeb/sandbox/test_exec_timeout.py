"""exec(timeout=N) is a total deadline on the streaming path too.

The executor sends an SSE keepalive every 10 s, so the per-read httpx timeout
alone never fires while a silent command runs: the budget must be enforced on
top of it, and the stream closed so the executor stops the command.
"""

import asyncio
import time
import unittest
from unittest.mock import patch

import httpx

from koyeb.sandbox.errors import SandboxTimeoutError
from koyeb.sandbox.exec import AsyncSandboxExecutor, SandboxExecutor
from koyeb.sandbox.executor_client import (
    AsyncSandboxClient,
    ConnectionInfo,
    SandboxClient,
)

_CONN = ConnectionInfo(public_url="https://sb.example", routing_key=None, secret="s")
_KEEPALIVE = b":keepalive\n\n"
_DONE = b'data: {"stream": "stdout", "data": "hi"}\n\ndata: {"code": 0, "error": false}\n\n'


class _SyncStream(httpx.SyncByteStream):
    """Sends a keepalive every `interval` seconds, `count` times, then ends."""

    def __init__(self, interval, count, tail=b""):
        self.interval, self.count, self.tail = interval, count, tail
        self.closed = False

    def __iter__(self):
        for _ in range(self.count):
            yield _KEEPALIVE
            time.sleep(self.interval)
        yield self.tail

    def close(self):
        self.closed = True


class _AsyncStream(httpx.AsyncByteStream):
    """Async twin of _SyncStream."""

    def __init__(self, interval, count, tail=b""):
        self.interval, self.count, self.tail = interval, count, tail
        self.closed = False

    async def __aiter__(self):
        for _ in range(self.count):
            yield _KEEPALIVE
            await asyncio.sleep(self.interval)
        yield self.tail

    async def aclose(self):
        self.closed = True


def _sync_client(stream):
    client = SandboxClient(_CONN)
    client._client = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, stream=stream))
    )
    return client


def _async_client(stream):
    client = AsyncSandboxClient(_CONN)
    client._client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, stream=stream))
    )
    return client


async def _collect(agen):
    return [event async for event in agen]


class TestSyncStreamingDeadline(unittest.TestCase):
    def test_keepalives_do_not_extend_total_timeout(self):
        stream = _SyncStream(interval=0.05, count=200)
        client = _sync_client(stream)
        start = time.monotonic()
        with self.assertRaises(SandboxTimeoutError):
            list(client.run_streaming("sleep 60", timeout=5, total_timeout=0.3))
        self.assertLess(time.monotonic() - start, 1.0)
        self.assertTrue(stream.closed)

    def test_without_total_timeout_stream_runs_to_the_end(self):
        client = _sync_client(_SyncStream(interval=0.05, count=4, tail=_DONE))
        events = list(client.run_streaming("echo hi", timeout=5))
        self.assertEqual(events[-1], {"code": 0, "error": False})

    def test_exec_timeout_raises_while_only_keepalives_arrive(self):
        stream = _SyncStream(interval=0.05, count=200)
        executor = SandboxExecutor(None)
        with patch.object(
            SandboxExecutor, "_get_client", return_value=_sync_client(stream)
        ):
            start = time.monotonic()
            with self.assertRaises(SandboxTimeoutError):
                executor("sleep 60", timeout=1)
        self.assertLess(time.monotonic() - start, 2.0)
        self.assertTrue(stream.closed)

    def test_exec_within_timeout_returns_result(self):
        stream = _SyncStream(interval=0.05, count=4, tail=_DONE)
        executor = SandboxExecutor(None)
        with patch.object(
            SandboxExecutor, "_get_client", return_value=_sync_client(stream)
        ):
            result = executor("echo hi", timeout=1)
        self.assertEqual((result.stdout, result.exit_code), ("hi", 0))


class TestAsyncStreamingDeadline(unittest.TestCase):
    def test_keepalives_do_not_extend_total_timeout(self):
        stream = _AsyncStream(interval=0.05, count=200)
        client = _async_client(stream)
        start = time.monotonic()
        with self.assertRaises(SandboxTimeoutError):
            asyncio.run(
                _collect(client.run_streaming("sleep 60", timeout=5, total_timeout=0.3))
            )
        self.assertLess(time.monotonic() - start, 1.0)
        self.assertTrue(stream.closed)

    def test_total_timeout_fires_during_silence(self):
        # Async enforcement does not wait for the next line: one keepalive, then
        # a 10 s silence, still times out at the deadline.
        stream = _AsyncStream(interval=10, count=1)
        client = _async_client(stream)
        start = time.monotonic()
        with self.assertRaises(SandboxTimeoutError):
            asyncio.run(
                _collect(client.run_streaming("sleep 60", timeout=30, total_timeout=0.3))
            )
        self.assertLess(time.monotonic() - start, 1.0)
        self.assertTrue(stream.closed)

    def test_without_total_timeout_stream_runs_to_the_end(self):
        client = _async_client(_AsyncStream(interval=0.05, count=4, tail=_DONE))
        events = asyncio.run(_collect(client.run_streaming("echo hi", timeout=5)))
        self.assertEqual(events[-1], {"code": 0, "error": False})

    def test_exec_timeout_raises_while_only_keepalives_arrive(self):
        stream = _AsyncStream(interval=0.05, count=200)
        executor = AsyncSandboxExecutor(None)

        async def run():
            return await executor("sleep 60", timeout=1)

        with patch.object(
            AsyncSandboxExecutor, "_get_async_client", return_value=_async_client(stream)
        ):
            start = time.monotonic()
            with self.assertRaises(SandboxTimeoutError):
                asyncio.run(run())
        self.assertLess(time.monotonic() - start, 2.0)
        self.assertTrue(stream.closed)


if __name__ == "__main__":
    unittest.main()
