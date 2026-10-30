import asyncio
import contextlib
import unittest
from unittest.mock import patch

import httpx

from koyeb.sandbox.executor_client import (
    AsyncSandboxClient,
    ConnectionInfo,
    SandboxClient,
)
from koyeb.sandbox.sandbox import AsyncSandbox, Sandbox
from koyeb.sandbox.errors import SandboxConnectionError, SandboxError


class TestGetClientWhenUrlUnavailable(unittest.TestCase):
    """A gone sandbox makes _get_sandbox_url() return None (the metadata/domain
    lookups swallow NotFound and return None). _get_client/_get_async_client must
    raise SandboxError in that case, as their docstring promises, rather than
    letting a raw ``TypeError: cannot unpack non-iterable NoneType object`` escape.
    """

    def test_get_client_raises_sandbox_error(self):
        sb = Sandbox.__new__(Sandbox)
        sb._client = None
        sb.sandbox_secret = None
        with patch.object(Sandbox, "_get_sandbox_url", return_value=None):
            with self.assertRaises(SandboxError):
                sb._get_client()

    def test_get_async_client_raises_sandbox_error(self):
        sb = AsyncSandbox.__new__(AsyncSandbox)
        sb._async_client = None
        sb.sandbox_secret = None
        with patch.object(AsyncSandbox, "_get_sandbox_url", return_value=None):
            with self.assertRaises(SandboxError):
                sb._get_async_client()


class TestRunStreamingConnectionLoss(unittest.TestCase):
    """A dropped connection mid-stream (e.g. the instance is torn down during a
    redeployment) must surface as SandboxConnectionError, not a raw httpx
    transport error.
    """

    _CONN = ConnectionInfo(
        public_url="https://sb.example", routing_key=None, secret="s"
    )

    def test_sync_run_streaming_wraps_transport_error(self):
        client = SandboxClient(self._CONN)
        with patch.object(
            client._client,
            "stream",
            side_effect=httpx.RemoteProtocolError("peer closed connection"),
        ):
            with self.assertRaises(SandboxConnectionError):
                list(client.run_streaming("echo hi"))

    def test_async_run_streaming_wraps_transport_error(self):
        client = AsyncSandboxClient(self._CONN)

        async def consume():
            async for _ in client.run_streaming("echo hi"):
                pass

        with patch.object(
            client._client,
            "stream",
            side_effect=httpx.RemoteProtocolError("peer closed connection"),
        ):
            with self.assertRaises(SandboxConnectionError):
                asyncio.run(consume())


class _FakeStreamResponse:
    """Enough of an httpx streaming response to drive run_streaming."""

    def __init__(self, lines):
        self.status_code = 200
        self._lines = lines

    def raise_for_status(self):
        pass

    def iter_lines(self):
        return iter(self._lines)


class _FakeAsyncStreamResponse:
    def __init__(self, lines):
        self.status_code = 200
        self._lines = lines

    def raise_for_status(self):
        pass

    async def aiter_lines(self):
        for line in self._lines:
            yield line


class TestRunStreamingSseParsing(unittest.TestCase):
    """Event-boundary parsing per the SSE format: multiple data: lines join
    with newlines, a blank line ends an event, and a trailing unterminated
    event is flushed at EOF."""

    _CONN = ConnectionInfo(
        public_url="https://sb.example", routing_key=None, secret="s"
    )

    _MULTI_LINE = [
        "event: output",
        'data: {"stream": "stdout",',
        'data: "data": "hi"}',
        "",
        'data: {"code": 0, "error": false}',
        "",
    ]
    _EXPECTED = [{"stream": "stdout", "data": "hi"}, {"code": 0, "error": False}]

    def _sync_events(self, lines):
        client = SandboxClient(self._CONN)

        @contextlib.contextmanager
        def fake_stream(*args, **kwargs):
            yield _FakeStreamResponse(lines)

        with patch.object(client._client, "stream", fake_stream):
            return list(client.run_streaming("echo hi"))

    def _async_events(self, lines):
        client = AsyncSandboxClient(self._CONN)

        class fake_stream:
            async def __aenter__(self):
                return _FakeAsyncStreamResponse(lines)

            async def __aexit__(self, *exc):
                return False

        async def consume():
            events = []
            async for event in client.run_streaming("echo hi"):
                events.append(event)
            return events

        with patch.object(client._client, "stream", lambda *a, **k: fake_stream()):
            return asyncio.run(consume())

    def test_multi_line_data_fields_join_with_newlines(self):
        self.assertEqual(self._sync_events(self._MULTI_LINE), self._EXPECTED)
        self.assertEqual(self._async_events(self._MULTI_LINE), self._EXPECTED)

    def test_crlf_line_endings_parse(self):
        # Worst case: the line iterator keeps the carriage returns.
        lines = [
            "event: output\r",
            'data: {"stream": "stdout", "data": "hi"}\r',
            "\r",
            'data: {"code": 0, "error": false}\r',
            "\r",
        ]
        self.assertEqual(self._sync_events(lines), self._EXPECTED)
        self.assertEqual(self._async_events(lines), self._EXPECTED)

    def test_unterminated_event_is_flushed_at_eof(self):
        self.assertEqual(self._sync_events(['data: {"code": 5}']), [{"code": 5}])
        self.assertEqual(self._async_events(['data: {"code": 5}']), [{"code": 5}])


if __name__ == "__main__":
    unittest.main()
