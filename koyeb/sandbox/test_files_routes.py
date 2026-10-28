"""Pins the raw-bytes /files transport on the executor clients.

The streamed routes (executor v0.0.24+) are a
raw-HTTP contract: query-parameter routes, real status codes with
``{"error": ...}`` bodies, and raw byte streams. These tests pin the client
side of that contract against httpx.MockTransport, the way
test_executor_retry.py pins the retry seam.
"""

import unittest

import httpx

from koyeb.sandbox.executor_client import (
    AsyncSandboxClient,
    ConnectionInfo,
    SandboxClient,
)
from koyeb.sandbox.errors import (
    SandboxError,
    SandboxRequestError,
    SandboxServiceError,
    SandboxTimeoutError,
)

_CONN = ConnectionInfo(public_url="https://sb.example", routing_key=None, secret="s")


def _make_sync_client(handler):
    client = SandboxClient(_CONN)
    client._client = httpx.Client(transport=httpx.MockTransport(handler))
    return client


def _make_async_client(handler):
    client = AsyncSandboxClient(_CONN)
    client._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return client


class TestFilesStat(unittest.TestCase):
    def test_sends_get_and_returns_entry(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(
                200,
                request=request,
                json={
                    "type": "file",
                    "size": 5,
                    "mode": "0644",
                    "mtime": "2026-10-27T10:00:00Z",
                },
            )

        entry = _make_sync_client(handler).files_stat("/tmp/a.txt")

        self.assertEqual(seen["method"], "GET")
        self.assertEqual(
            seen["url"], "https://sb.example/files/stat?path=%2Ftmp%2Fa.txt"
        )
        self.assertEqual(entry["type"], "file")
        self.assertEqual(entry["size"], 5)
        self.assertEqual(entry["mode"], "0644")

    def test_404_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                404, request=request, json={"error": "file does not exist"}
            )

        with self.assertRaises(SandboxRequestError) as ctx:
            _make_sync_client(handler).files_stat("/tmp/missing.txt")

        self.assertEqual(ctx.exception.status_code, 404)


class TestAsyncFilesStat(unittest.IsolatedAsyncioTestCase):
    async def test_sends_get_and_returns_entry(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(
                200,
                request=request,
                json={"type": "dir", "size": 0, "mode": "0755"},
            )

        entry = await _make_async_client(handler).files_stat("/tmp")

        self.assertEqual(seen["method"], "GET")
        self.assertEqual(seen["url"], "https://sb.example/files/stat?path=%2Ftmp")
        self.assertEqual(entry["type"], "dir")


class TestFilesPut(unittest.TestCase):
    def test_streams_body_and_returns_commit_reply(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["content_type"] = request.headers.get("Content-Type")
            seen["sha_header"] = request.headers.get("X-Content-SHA256")
            seen["body"] = request.read()
            return httpx.Response(
                200, request=request, json={"size": 3, "sha256": "deadbeef"}
            )

        reply = _make_sync_client(handler).files_put(
            "/tmp/a.txt", b"xyz", mode="0600", parents=True, sha256="deadbeef"
        )

        self.assertEqual(seen["method"], "PUT")
        self.assertEqual(
            seen["url"],
            "https://sb.example/files?path=%2Ftmp%2Fa.txt&mode=0600&parents=1",
        )
        self.assertEqual(seen["content_type"], "application/octet-stream")
        self.assertEqual(seen["sha_header"], "deadbeef")
        self.assertEqual(seen["body"], b"xyz")
        self.assertEqual(reply, {"size": 3, "sha256": "deadbeef"})

    def test_accepts_iterable_content(self):
        seen = {}

        def handler(request):
            seen["body"] = request.read()
            return httpx.Response(
                200, request=request, json={"size": 6, "sha256": "sum"}
            )

        def chunks():
            yield b"ab"
            yield b"cdef"

        _make_sync_client(handler).files_put("/tmp/a.txt", chunks())

        self.assertEqual(seen["body"], b"abcdef")

    def test_mid_stream_failure_is_not_retried(self):
        calls = []

        def handler(request):
            calls.append(1)
            raise httpx.ReadError("reset mid-stream", request=request)

        with self.assertRaises(SandboxError):
            _make_sync_client(handler).files_put("/tmp/a.txt", b"xyz")

        # A streamed body cannot be replayed: only a connect-time failure
        # (the request never left) is retried.
        self.assertEqual(len(calls), 1)


class TestAsyncFilesPut(unittest.IsolatedAsyncioTestCase):
    async def test_streams_body_and_returns_commit_reply(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["content_type"] = request.headers.get("Content-Type")
            seen["sha_header"] = request.headers.get("X-Content-SHA256")
            seen["body"] = request.read()
            return httpx.Response(
                200, request=request, json={"size": 3, "sha256": "deadbeef"}
            )

        reply = await _make_async_client(handler).files_put(
            "/tmp/a.txt", b"xyz", mode="0600", parents=True, sha256="deadbeef"
        )

        self.assertEqual(seen["method"], "PUT")
        self.assertEqual(
            seen["url"],
            "https://sb.example/files?path=%2Ftmp%2Fa.txt&mode=0600&parents=1",
        )
        self.assertEqual(seen["content_type"], "application/octet-stream")
        self.assertEqual(seen["sha_header"], "deadbeef")
        self.assertEqual(seen["body"], b"xyz")
        self.assertEqual(reply, {"size": 3, "sha256": "deadbeef"})

    async def test_accepts_iterable_content(self):
        seen = {}

        def handler(request):
            seen["body"] = request.read()
            return httpx.Response(
                200, request=request, json={"size": 6, "sha256": "sum"}
            )

        def chunks():
            yield b"ab"
            yield b"cdef"

        reply = await _make_async_client(handler).files_put("/tmp/a.txt", chunks())

        self.assertEqual(seen["body"], b"abcdef")
        self.assertEqual(reply, {"size": 6, "sha256": "sum"})

    async def test_accepts_file_object_content(self):
        import io

        seen = {}

        def handler(request):
            seen["body"] = request.read()
            return httpx.Response(
                200, request=request, json={"size": 3, "sha256": "sum"}
            )

        reply = await _make_async_client(handler).files_put(
            "/tmp/a.txt", io.BytesIO(b"xyz")
        )

        self.assertEqual(seen["body"], b"xyz")
        self.assertEqual(reply, {"size": 3, "sha256": "sum"})


class TestFilesRead(unittest.TestCase):
    def test_yields_chunks_from_get(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(200, request=request, content=b"abcdef")

        chunks = list(_make_sync_client(handler).files_read("/tmp/a.txt"))

        self.assertEqual(seen["method"], "GET")
        self.assertEqual(seen["url"], "https://sb.example/files?path=%2Ftmp%2Fa.txt")
        self.assertEqual(b"".join(chunks), b"abcdef")

    def test_404_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                404, request=request, json={"error": "file does not exist"}
            )

        with self.assertRaises(SandboxRequestError) as ctx:
            list(_make_sync_client(handler).files_read("/tmp/missing.txt"))

        self.assertEqual(ctx.exception.status_code, 404)


class TestAsyncFilesRead(unittest.IsolatedAsyncioTestCase):
    async def test_yields_chunks_from_get(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(200, request=request, content=b"abcdef")

        chunks = []
        async for chunk in _make_async_client(handler).files_read("/tmp/a.txt"):
            chunks.append(chunk)

        self.assertEqual(seen["method"], "GET")
        self.assertEqual(seen["url"], "https://sb.example/files?path=%2Ftmp%2Fa.txt")
        self.assertEqual(b"".join(chunks), b"abcdef")


class TestHasFilesRoutes(unittest.TestCase):
    def test_404_means_legacy_cached_and_warned_once(self):
        calls = []

        def handler(request):
            calls.append(str(request.url))
            return httpx.Response(404, request=request, text="404 page not found")

        client = _make_sync_client(handler)

        with self.assertLogs("koyeb.sandbox.executor_client", level="WARNING") as logs:
            self.assertFalse(client.has_files_routes())
            self.assertFalse(client.has_files_routes())

        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0], "https://sb.example/files/stat")
        self.assertEqual(len([r for r in logs.output if "legacy" in r]), 1)

    def test_400_means_new_routes(self):
        def handler(request):
            return httpx.Response(
                400, request=request, json={"error": "path is required"}
            )

        client = _make_sync_client(handler)

        self.assertTrue(client.has_files_routes())
        self.assertTrue(client.has_files_routes())


class TestAsyncHasFilesRoutes(unittest.IsolatedAsyncioTestCase):
    async def test_404_means_legacy_cached_and_warned_once(self):
        calls = []

        def handler(request):
            calls.append(str(request.url))
            return httpx.Response(404, request=request, text="404 page not found")

        client = _make_async_client(handler)

        with self.assertLogs("koyeb.sandbox.executor_client", level="WARNING") as logs:
            self.assertFalse(await client.has_files_routes())
            self.assertFalse(await client.has_files_routes())

        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0], "https://sb.example/files/stat")
        self.assertEqual(len([r for r in logs.output if "legacy" in r]), 1)


class TestProbeTransientStatuses(unittest.TestCase):
    def test_429_raises_without_caching(self):
        calls = []

        def handler(request):
            calls.append(str(request.url))
            return httpx.Response(429, request=request, text="slow down")

        client = _make_sync_client(handler)
        for _ in range(2):
            with self.assertRaises(SandboxError):
                client.has_files_routes()
        # Uncached: an auth or rate-limit blip says nothing about the
        # routes, so every call probes again instead of poisoning the handle.
        self.assertEqual(len(calls), 2)


class TestAsyncProbeTransientStatuses(unittest.IsolatedAsyncioTestCase):
    async def test_401_raises_without_caching(self):
        calls = []

        def handler(request):
            calls.append(str(request.url))
            return httpx.Response(401, request=request, text="no")

        client = _make_async_client(handler)
        for _ in range(2):
            with self.assertRaises(SandboxError):
                await client.has_files_routes()
        self.assertEqual(len(calls), 2)


class TestHasFilesRoutesPositiveArms(unittest.TestCase):
    def test_2xx_means_routes_available(self):
        def handler(request):
            # Unexpected shape for a body-less stat, but a 2xx can only come
            # from a live /files/stat route.
            return httpx.Response(200, request=request, json={"type": "file"})

        client = _make_sync_client(handler)
        self.assertTrue(client.has_files_routes())


class TestAsyncHasFilesRoutesPositiveArms(unittest.IsolatedAsyncioTestCase):
    async def test_400_means_new_routes(self):
        def handler(request):
            return httpx.Response(
                400, request=request, json={"error": "path is required"}
            )

        client = _make_async_client(handler)
        self.assertTrue(await client.has_files_routes())
        self.assertTrue(await client.has_files_routes())

    async def test_2xx_means_routes_available(self):
        def handler(request):
            return httpx.Response(200, request=request, json={"type": "file"})

        client = _make_async_client(handler)
        self.assertTrue(await client.has_files_routes())


class TestFilesReadStatusArms(unittest.TestCase):
    def test_500_wraps_service_error(self):
        def handler(request):
            return httpx.Response(500, request=request, json={"error": "boom"})

        with self.assertRaises(SandboxServiceError) as cm:
            list(_make_sync_client(handler).files_read("/a"))

        self.assertEqual(cm.exception.status_code, 500)


class TestAsyncFilesReadStatusArms(unittest.IsolatedAsyncioTestCase):
    async def test_404_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                404, request=request, json={"error": "file does not exist"}
            )

        client = _make_async_client(handler)
        with self.assertRaises(SandboxRequestError) as cm:
            async for _ in client.files_read("/missing"):
                pass
        self.assertEqual(cm.exception.status_code, 404)


class TestFilesRead400Boundary(unittest.TestCase):
    """A 400 is the probe's own answer code: the read stream must raise
    on it, not yield the error body as content."""

    def test_400_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                400, request=request, json={"error": "path is required"}
            )

        with self.assertRaises(SandboxRequestError) as cm:
            list(_make_sync_client(handler).files_read("/a"))

        self.assertEqual(cm.exception.status_code, 400)


class TestAsyncFilesRead400Boundary(unittest.IsolatedAsyncioTestCase):
    async def test_400_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                400, request=request, json={"error": "path is required"}
            )

        with self.assertRaises(SandboxRequestError) as cm:
            async for _ in _make_async_client(handler).files_read("/a"):
                pass

        self.assertEqual(cm.exception.status_code, 400)


class TestFilesPutParents(unittest.TestCase):
    def test_parents_flag_is_sent(self):
        seen = {}

        def handler(request):
            seen["url"] = str(request.url)
            return httpx.Response(
                200, request=request, json={"size": 3, "sha256": "sum"}
            )

        _make_sync_client(handler).files_put("/tmp/a/b.txt", b"abc", parents=True)

        self.assertEqual(
            seen["url"],
            "https://sb.example/files?path=%2Ftmp%2Fa%2Fb.txt&parents=1",
        )


class TestFilesRouteTimeouts(unittest.TestCase):
    """The timeout error names the bound that fired: the 60 s idle bound
    on the streamed /files routes, the 30 s total cap elsewhere."""

    def test_files_route_names_idle_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            _make_sync_client(handler).files_put("/a", b"abc")

        self.assertEqual(str(cm.exception), "Request timed out after 60s")

    def test_legacy_call_names_total_cap(self):
        def handler(request):
            raise httpx.ReadTimeout("slow", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            _make_sync_client(handler).read_file("/a")

        self.assertEqual(str(cm.exception), "Request timed out after 30s")


class TestAsyncFilesRouteTimeouts(unittest.IsolatedAsyncioTestCase):
    async def test_files_route_names_idle_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            await _make_async_client(handler).files_put("/a", b"abc")

        self.assertEqual(str(cm.exception), "Request timed out after 60s")


class TestFilesReadTimeouts(unittest.TestCase):
    """An idle stall mid-download is a timeout by name, not a generic
    connection failure; a reset mid-stream stays generic."""

    def test_idle_stall_names_the_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            list(_make_sync_client(handler).files_read("/a"))

        self.assertEqual(str(cm.exception), "Request timed out after 60s")

    def test_reset_mid_stream_wraps_generic(self):
        def handler(request):
            raise httpx.ReadError("reset", request=request)

        with self.assertRaises(SandboxError) as cm:
            list(_make_sync_client(handler).files_read("/a"))

        self.assertIn("Request to sandbox executor failed", str(cm.exception))


class TestAsyncFilesReadTimeouts(unittest.IsolatedAsyncioTestCase):
    async def test_idle_stall_names_the_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            async for _ in _make_async_client(handler).files_read("/a"):
                pass

        self.assertEqual(str(cm.exception), "Request timed out after 60s")

    async def test_reset_mid_stream_wraps_generic(self):
        def handler(request):
            raise httpx.ReadError("reset", request=request)

        with self.assertRaises(SandboxError) as cm:
            async for _ in _make_async_client(handler).files_read("/a"):
                pass

        self.assertIn("Request to sandbox executor failed", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
