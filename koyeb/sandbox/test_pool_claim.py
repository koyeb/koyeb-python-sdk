import asyncio
import os
import threading
import unittest
from enum import Enum
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import urllib3

from koyeb.api.exceptions import ApiException, NotFoundException
from koyeb.api_async.exceptions import ApiException as AsyncApiException
from koyeb.api_async.exceptions import NotFoundException as AsyncNotFoundException
from koyeb.api_async.models.get_pool_claim_reply import (
    GetPoolClaimReply as AsyncGetPoolClaimReply,
)
from koyeb.api_async.models.get_service_reply import (
    GetServiceReply as AsyncGetServiceReply,
)
from koyeb.api_async.models.pool_claim import PoolClaim as AsyncPoolClaimResource
from koyeb.api_async.models.pool_claim_reply import (
    PoolClaimReply as AsyncPoolClaimReply,
)
from koyeb.api_async.models.pool_claim_status import (
    PoolClaimStatus as AsyncPoolClaimStatus,
)
from koyeb.api_async.models.service import Service as AsyncService
from koyeb.api_async.models.service_status import (
    ServiceStatus as AsyncServiceStatus,
)
from koyeb.api.models.get_pool_claim_reply import GetPoolClaimReply
from koyeb.api.models.get_service_reply import GetServiceReply
from koyeb.api.models.pool_claim import PoolClaim as PoolClaimResource
from koyeb.api.models.pool_claim_reply import PoolClaimReply
from koyeb.api.models.pool_claim_status import PoolClaimStatus
from koyeb.api.models.service import Service
from koyeb.api.models.service_status import ServiceStatus
from koyeb.sandbox.pool import (
    AsyncPoolClaim,
    PoolClaim,
    _classify_service_status,
)
from koyeb.sandbox.utils import (
    DEFAULT_HTTP_TIMEOUT,
    SandboxClaimError,
    SandboxTimeoutError,
)
from pydantic import ValidationError

POOL_ID = "pool-1"
SERVICE_ID = "svc-1"


def _claim_reply(prewarmed: bool = True) -> PoolClaimReply:
    return PoolClaimReply(claim_id="cl-1", service_id=SERVICE_ID, prewarmed=prewarmed)


def _async_claim_reply(prewarmed: bool = True) -> AsyncPoolClaimReply:
    return AsyncPoolClaimReply(
        claim_id="cl-1", service_id=SERVICE_ID, prewarmed=prewarmed
    )


def _claim_resource() -> PoolClaimResource:
    return PoolClaimResource(
        id="cl-1",
        pool_id=POOL_ID,
        service_id=SERVICE_ID,
        request_id="req-1",
        status=PoolClaimStatus.FULFILLED,
    )


def _async_claim_resource() -> AsyncPoolClaimResource:
    return AsyncPoolClaimResource(
        id="cl-1",
        pool_id=POOL_ID,
        service_id=SERVICE_ID,
        request_id="req-1",
        status=AsyncPoolClaimStatus.FULFILLED,
    )


def _async_service_reply(status) -> AsyncGetServiceReply:
    return AsyncGetServiceReply(service=AsyncService(id=SERVICE_ID, status=status))


def _service_reply(status: ServiceStatus) -> GetServiceReply:
    return GetServiceReply(service=Service(id=SERVICE_ID, status=status))


def _sync_clients(claim_mock):
    clients = MagicMock()
    clients.pool_claims.claim = claim_mock
    return clients


def _async_clients(claim_mock):
    clients = MagicMock()

    async def claim(**kwargs):
        return await claim_mock(**kwargs)

    clients.pool_claims.claim = claim
    return clients


class TestPoolClaim(unittest.TestCase):
    """PoolClaim.claim: request_id handling, retries, and result mapping."""

    def test_claim_passes_explicit_request_id(self):
        claim_mock = MagicMock(return_value=_claim_reply())
        with patch(
            "koyeb.sandbox.pool.get_api_clients", return_value=_sync_clients(claim_mock)
        ):
            claim = PoolClaim.claim(POOL_ID, request_id="req-42", wait_ready=False)
        body = claim_mock.call_args.kwargs["body"]
        self.assertEqual(body.pool_id, POOL_ID)
        self.assertEqual(body.request_id, "req-42")
        self.assertEqual(claim.request_id, "req-42")
        self.assertEqual(claim.claim_id, "cl-1")
        self.assertEqual(claim.service_id, SERVICE_ID)
        self.assertTrue(claim.prewarmed)

    def test_claim_generates_request_id_once(self):
        claim_mock = MagicMock(return_value=_claim_reply())
        with patch(
            "koyeb.sandbox.pool.get_api_clients", return_value=_sync_clients(claim_mock)
        ):
            claim = PoolClaim.claim(POOL_ID, wait_ready=False)
        self.assertTrue(claim.request_id)
        self.assertEqual(
            claim_mock.call_args.kwargs["body"].request_id, claim.request_id
        )

    def test_claim_preserves_request_id_across_retries(self):
        replies = [
            ApiException(status=503, reason="Service Unavailable"),
            ApiException(status=502, reason="Bad Gateway"),
            _claim_reply(),
        ]
        bodies = []

        def claim_mock(**kwargs):
            bodies.append(kwargs["body"])
            reply = replies.pop(0)
            if isinstance(reply, Exception):
                raise reply
            return reply

        with (
            patch(
                "koyeb.sandbox.pool.get_api_clients",
                return_value=_sync_clients(claim_mock),
            ),
            patch("time.sleep"),
        ):
            claim = PoolClaim.claim(POOL_ID, wait_ready=False)
        self.assertEqual(claim.service_id, SERVICE_ID)
        self.assertEqual(len(replies), 0)  # third attempt succeeded
        # The same request_id was replayed on every attempt
        self.assertEqual(len(bodies), 3)
        self.assertEqual(
            {(b.pool_id, b.request_id) for b in bodies}, {(POOL_ID, claim.request_id)}
        )

    def test_claim_retries_transport_errors(self):
        attempts = [
            urllib3.exceptions.MaxRetryError(None, "/v1/claim"),  # type: ignore[arg-type]
            _claim_reply(),
        ]

        def claim_mock(**kwargs):
            reply = attempts.pop(0)
            if isinstance(reply, Exception):
                raise reply
            return reply

        with (
            patch(
                "koyeb.sandbox.pool.get_api_clients",
                return_value=_sync_clients(claim_mock),
            ),
            patch("time.sleep"),
        ):
            claim = PoolClaim.claim(POOL_ID, request_id="req-x", wait_ready=False)
        self.assertEqual(claim.service_id, SERVICE_ID)

    def test_claim_does_not_retry_client_errors(self):
        claim_mock = MagicMock(
            side_effect=ApiException(status=404, reason="pool not found")
        )
        with (
            patch(
                "koyeb.sandbox.pool.get_api_clients",
                return_value=_sync_clients(claim_mock),
            ),
            patch("time.sleep"),
        ):
            with self.assertRaises(SandboxClaimError):
                PoolClaim.claim(POOL_ID, wait_ready=False)
        self.assertEqual(claim_mock.call_count, 1)

    def test_claim_raises_when_exhausted(self):
        claim_mock = MagicMock(
            side_effect=ApiException(status=503, reason="Service Unavailable")
        )
        with (
            patch(
                "koyeb.sandbox.pool.get_api_clients",
                return_value=_sync_clients(claim_mock),
            ),
            patch("time.sleep"),
        ):
            with self.assertRaises(SandboxClaimError):
                PoolClaim.claim(POOL_ID, wait_ready=False)
        self.assertEqual(claim_mock.call_count, 3)  # _CLAIM_MAX_ATTEMPTS

    def test_claim_raises_when_service_id_missing(self):
        claim_mock = MagicMock(
            return_value=PoolClaimReply(claim_id="cl-1", prewarmed=True)
        )
        with patch(
            "koyeb.sandbox.pool.get_api_clients", return_value=_sync_clients(claim_mock)
        ):
            with self.assertRaises(SandboxClaimError):
                PoolClaim.claim(POOL_ID, wait_ready=False)

    def test_claim_raises_when_claim_id_missing(self):
        claim_mock = MagicMock(
            return_value=PoolClaimReply(service_id=SERVICE_ID, prewarmed=True)
        )
        with patch(
            "koyeb.sandbox.pool.get_api_clients", return_value=_sync_clients(claim_mock)
        ):
            with self.assertRaises(SandboxClaimError):
                PoolClaim.claim(POOL_ID, wait_ready=False)

    def test_claim_retries_rate_limited_requests(self):
        replies = [
            ApiException(status=429, reason="Too Many Requests"),
            _claim_reply(),
        ]

        def claim_mock(**kwargs):
            reply = replies.pop(0)
            if isinstance(reply, Exception):
                raise reply
            return reply

        with (
            patch(
                "koyeb.sandbox.pool.get_api_clients",
                return_value=_sync_clients(claim_mock),
            ),
            patch("time.sleep"),
        ):
            claim = PoolClaim.claim(POOL_ID, wait_ready=False)
        self.assertEqual(claim.service_id, SERVICE_ID)

    def test_claim_exhausted_surfaces_last_error(self):
        claim_mock = MagicMock(
            side_effect=[
                ApiException(status=503, reason="first"),
                ApiException(status=503, reason="second"),
                ApiException(status=503, reason="third"),
            ]
        )
        with (
            patch(
                "koyeb.sandbox.pool.get_api_clients",
                return_value=_sync_clients(claim_mock),
            ),
            patch("time.sleep"),
        ):
            with self.assertRaises(SandboxClaimError) as ctx:
                PoolClaim.claim(POOL_ID, wait_ready=False)
        self.assertEqual(claim_mock.call_count, 3)
        self.assertIn("third", str(ctx.exception))
        self.assertEqual(ctx.exception.__cause__.reason, "third")  # type: ignore[union-attr]

    def test_claim_requires_api_token(self):
        with patch.dict(os.environ):
            os.environ.pop("KOYEB_API_TOKEN", None)
            with self.assertRaises(ValueError):
                PoolClaim.claim(POOL_ID, wait_ready=False)

    def test_claim_requires_pool_id(self):
        with self.assertRaises(ValueError):
            PoolClaim.claim("")

    def test_claim_cold_path_waits_until_ready(self):
        # Full wiring: claim(wait_ready=True) polls the claimed service and
        # returns once it becomes ready — no internals mocked.
        claim_mock = MagicMock(return_value=_claim_reply(prewarmed=False))
        get_service = MagicMock(
            side_effect=[
                _service_reply(ServiceStatus.STARTING),
                _service_reply(ServiceStatus.HEALTHY),
            ]
        )
        clients = MagicMock()
        clients.pool_claims.claim = claim_mock
        clients.services.get_service = get_service
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            claim = PoolClaim.claim(
                POOL_ID, wait_ready=True, timeout=10, poll_interval=0.01
            )
        self.assertEqual(claim.service_id, SERVICE_ID)
        self.assertFalse(claim.prewarmed)

    def test_claim_error_carries_request_id(self):
        # A failed claim must expose its request_id so the caller can replay
        # the same (pool_id, request_id) instead of claiming twice.
        claim_mock = MagicMock(
            side_effect=ApiException(status=404, reason="pool not found")
        )
        with (
            patch(
                "koyeb.sandbox.pool.get_api_clients",
                return_value=_sync_clients(claim_mock),
            ),
            patch("time.sleep"),
        ):
            with self.assertRaises(SandboxClaimError) as ctx:
                PoolClaim.claim(POOL_ID, request_id="req-z", wait_ready=False)
        self.assertEqual(ctx.exception.request_id, "req-z")
        self.assertIn("req-z", str(ctx.exception))

    def test_claim_prewarmed_missing_defaults_false(self):
        claim_mock = MagicMock(
            return_value=PoolClaimReply(claim_id="cl-1", service_id=SERVICE_ID)
        )
        with patch(
            "koyeb.sandbox.pool.get_api_clients", return_value=_sync_clients(claim_mock)
        ):
            claim = PoolClaim.claim(POOL_ID, wait_ready=False)
        self.assertFalse(claim.prewarmed)

    def test_claim_rejects_invalid_poll_interval(self):
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                PoolClaim.claim(POOL_ID, poll_interval=bad, wait_ready=False)

    def test_repr_includes_identity_fields(self):
        claim_mock = MagicMock(return_value=_claim_reply())
        with patch(
            "koyeb.sandbox.pool.get_api_clients", return_value=_sync_clients(claim_mock)
        ):
            claim = PoolClaim.claim(POOL_ID, wait_ready=False)
        self.assertIn("claim_id='cl-1'", repr(claim))
        self.assertIn(f"service_id='{SERVICE_ID}'", repr(claim))
        self.assertIn("prewarmed=True", repr(claim))

    def test_claim_wait_ready_false_does_not_poll(self):
        claim_mock = MagicMock(return_value=_claim_reply())
        clients = MagicMock()
        clients.pool_claims.claim = claim_mock
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            claim = PoolClaim.claim(POOL_ID, wait_ready=False)
        self.assertEqual(claim.service_id, SERVICE_ID)
        clients.services.get_service.assert_not_called()

    def test_claim_wait_ready_timeout(self):
        # The timeout argument governs the real poll loop: a never-ready
        # service fails the claim with SandboxTimeoutError.
        claim_mock = MagicMock(return_value=_claim_reply(prewarmed=False))
        get_service = MagicMock(return_value=_service_reply(ServiceStatus.STARTING))
        clients = MagicMock()
        clients.pool_claims.claim = claim_mock
        clients.services.get_service = get_service
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            with self.assertRaises(SandboxTimeoutError):
                PoolClaim.claim(POOL_ID, wait_ready=True, timeout=1, poll_interval=0.01)


class TestPoolClaimGetClaim(unittest.TestCase):
    """PoolClaim.get_claim: fetch a claim resource by id."""

    def test_get_claim_fetches_claim_by_id(self):
        get_claim_mock = MagicMock(
            return_value=GetPoolClaimReply(claim=_claim_resource())
        )
        clients = MagicMock()
        clients.pool_claims.get_claim = get_claim_mock
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            resource = PoolClaim.get_claim("cl-1", request_id="req-1")
        self.assertEqual(resource.id, "cl-1")
        self.assertEqual(resource.service_id, SERVICE_ID)
        self.assertEqual(get_claim_mock.call_args.kwargs["claim_id"], "cl-1")
        self.assertEqual(get_claim_mock.call_args.kwargs["request_id"], "req-1")

    def test_get_claim_omits_request_id_when_absent(self):
        get_claim_mock = MagicMock(
            return_value=GetPoolClaimReply(claim=_claim_resource())
        )
        clients = MagicMock()
        clients.pool_claims.get_claim = get_claim_mock
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            PoolClaim.get_claim("cl-1")
        self.assertIsNone(get_claim_mock.call_args.kwargs["request_id"])

    def test_get_claim_requires_claim_id(self):
        with self.assertRaises(ValueError):
            PoolClaim.get_claim("")


class TestPoolClaimWaitReady(unittest.TestCase):
    """PoolClaim.wait_ready: Get Service polling until ready or terminal."""

    def _claim(self) -> PoolClaim:
        return PoolClaim(
            pool_id=POOL_ID,
            claim_id="cl-1",
            service_id=SERVICE_ID,
            request_id="req-1",
            prewarmed=False,
        )

    def test_wait_ready_returns_true_on_healthy(self):
        clients = MagicMock()
        clients.services.get_service = MagicMock(
            return_value=_service_reply(ServiceStatus.HEALTHY)
        )
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            self.assertTrue(self._claim().wait_ready(timeout=5))

    def test_wait_ready_returns_true_on_degraded(self):
        # DEGRADED is usable for a claim: its active deployment
        # is healthy and serving traffic.
        clients = MagicMock()
        clients.services.get_service = MagicMock(
            return_value=_service_reply(ServiceStatus.DEGRADED)
        )
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            self.assertTrue(self._claim().wait_ready(timeout=5))

    def test_wait_ready_polls_until_healthy(self):
        statuses = [
            _service_reply(ServiceStatus.STARTING),
            _service_reply(ServiceStatus.RESUMING),
            _service_reply(ServiceStatus.HEALTHY),
        ]
        clients = MagicMock()
        clients.services.get_service = MagicMock(side_effect=statuses)
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            self.assertTrue(self._claim().wait_ready(timeout=5, poll_interval=0.01))

    def test_wait_ready_raises_on_terminal_status(self):
        for status in (
            ServiceStatus.UNHEALTHY,
            ServiceStatus.DELETING,
            ServiceStatus.DELETED,
            ServiceStatus.PAUSING,
            ServiceStatus.PAUSED,
        ):
            clients = MagicMock()
            clients.services.get_service = MagicMock(
                return_value=_service_reply(status)
            )
            with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
                with self.assertRaises(SandboxClaimError):
                    self._claim().wait_ready(timeout=5)

    def test_wait_ready_polls_through_404(self):
        # 404 is treated as transient: keep polling to timeout
        # rather than failing the claim on a possibly racy lookup.
        statuses = [
            NotFoundException(status=404, reason="Not Found"),
            _service_reply(ServiceStatus.HEALTHY),
        ]
        clients = MagicMock()
        clients.services.get_service = MagicMock(side_effect=statuses)
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            self.assertTrue(self._claim().wait_ready(timeout=5))

    def test_wait_ready_returns_false_on_timeout(self):
        clients = MagicMock()
        clients.services.get_service = MagicMock(
            return_value=_service_reply(ServiceStatus.STARTING)
        )
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            self.assertFalse(self._claim().wait_ready(timeout=1, poll_interval=0.01))

    def test_wait_ready_rejects_invalid_poll_interval(self):
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                self._claim().wait_ready(poll_interval=bad)

    def test_wait_ready_raises_on_unclassifiable_status(self):
        # An unknown Service.Status fails deserialization before reaching the
        # classifier; fail closed fast instead of polling to timeout.
        clients = MagicMock()
        clients.services.get_service = MagicMock(side_effect=_status_validation_error())
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            with self.assertRaises(SandboxClaimError) as ctx:
                self._claim().wait_ready(timeout=5)
        self.assertEqual(ctx.exception.request_id, "req-1")

    def test_wait_ready_treats_other_schema_errors_as_transient(self):
        # A schema failure on a non-status field is transient: keep polling.
        clients = MagicMock()
        clients.services.get_service = MagicMock(
            side_effect=[
                _other_field_validation_error(),
                _service_reply(ServiceStatus.HEALTHY),
            ]
        )
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            self.assertTrue(self._claim().wait_ready(timeout=5))

    def test_wait_ready_returns_false_on_persistent_errors(self):
        # Get Service failing for the whole budget is fail-closed: the claim
        # never reports ready.
        clients = MagicMock()
        clients.services.get_service = MagicMock(
            side_effect=ApiException(status=500, reason="Server Error")
        )
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            self.assertFalse(self._claim().wait_ready(timeout=1, poll_interval=0.01))

    def test_wait_ready_passes_http_timeout_to_get_service(self):
        # Without an explicit request timeout the sync client would block
        # indefinitely inside a single poll, defeating the wait timeout.
        clients = MagicMock()
        clients.services.get_service = MagicMock(
            return_value=_service_reply(ServiceStatus.HEALTHY)
        )
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            self.assertTrue(self._claim().wait_ready(timeout=5))
        self.assertEqual(
            clients.services.get_service.call_args.kwargs.get("_request_timeout"),
            DEFAULT_HTTP_TIMEOUT,
        )

    def test_wait_ready_swallows_transient_errors(self):
        statuses = [
            ApiException(status=500, reason="Server Error"),
            _service_reply(ServiceStatus.HEALTHY),
        ]
        clients = MagicMock()
        clients.services.get_service = MagicMock(side_effect=statuses)
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            self.assertTrue(self._claim().wait_ready(timeout=5))

    def test_wait_ready_stops_immediately_on_cancel_event(self):
        clients = MagicMock()
        clients.services.get_service = MagicMock(
            return_value=_service_reply(ServiceStatus.HEALTHY)
        )
        cancel = threading.Event()
        cancel.set()
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            self.assertFalse(self._claim().wait_ready(timeout=5, cancel=cancel))
        self.assertEqual(clients.services.get_service.call_count, 0)

    def test_wait_ready_keeps_polling_when_status_missing(self):
        replies = [
            GetServiceReply(service=Service(id=SERVICE_ID, status=None)),
            _service_reply(ServiceStatus.HEALTHY),
        ]
        clients = MagicMock()
        clients.services.get_service = MagicMock(side_effect=replies)
        with patch("koyeb.sandbox.pool.get_api_clients", return_value=clients):
            self.assertTrue(self._claim().wait_ready(timeout=5, poll_interval=0.01))
        self.assertEqual(clients.services.get_service.call_count, 2)


class TestAsyncPoolClaim(unittest.TestCase):
    """AsyncPoolClaim: async claim retries and wait_ready polling."""

    def _cold_path_clients(self):
        """Clients whose claim returns a cold claim and service goes
        STARTING -> HEALTHY."""

        async def claim_mock(**kwargs):
            return _async_claim_reply(prewarmed=False)

        clients = MagicMock()
        clients.pool_claims.claim = claim_mock
        clients.services.get_service = _async_side_effect(
            [
                _async_service_reply(AsyncServiceStatus.STARTING),
                _async_service_reply(AsyncServiceStatus.HEALTHY),
            ]
        )
        return clients

    def test_claim_cold_path_waits_until_ready(self):
        # Full wiring with the real async generated models: claim polls the
        # claimed service and returns once it becomes ready.
        clients = self._cold_path_clients()
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            claim = asyncio.run(
                AsyncPoolClaim.claim(
                    POOL_ID, wait_ready=True, timeout=10, poll_interval=0.01
                )
            )
        self.assertEqual(claim.service_id, SERVICE_ID)
        self.assertFalse(claim.prewarmed)

    def test_claim_preserves_request_id_across_retries(self):
        replies = [
            AsyncApiException(status=503, reason="Service Unavailable"),
            httpx.ConnectError("connection refused"),
            _async_claim_reply(),
        ]
        bodies = []

        async def claim_mock(**kwargs):
            bodies.append(kwargs["body"])
            reply = replies.pop(0)
            if isinstance(reply, Exception):
                raise reply
            return reply

        with (
            patch(
                "koyeb.sandbox.pool.get_async_api_clients",
                return_value=_async_clients(claim_mock),
            ),
            patch("asyncio.sleep"),
        ):
            claim = asyncio.run(AsyncPoolClaim.claim(POOL_ID, wait_ready=False))
        self.assertEqual(claim.service_id, SERVICE_ID)
        self.assertTrue(claim.request_id)
        self.assertIsInstance(claim, AsyncPoolClaim)
        # The same request_id was replayed on every attempt
        self.assertEqual(len(bodies), 3)
        self.assertEqual(
            {(b.pool_id, b.request_id) for b in bodies}, {(POOL_ID, claim.request_id)}
        )

    def test_claim_does_not_retry_client_errors(self):
        calls = []

        async def claim_mock(**kwargs):
            calls.append(kwargs)
            raise AsyncApiException(status=400, reason="bad request")

        clients = _async_clients(claim_mock)
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            with self.assertRaises(SandboxClaimError):
                asyncio.run(AsyncPoolClaim.claim(POOL_ID))
        self.assertEqual(len(calls), 1)

    def test_claim_passes_explicit_request_id(self):
        bodies = []

        async def claim_mock(**kwargs):
            bodies.append(kwargs["body"])
            return _async_claim_reply()

        clients = _async_clients(claim_mock)
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            claim = asyncio.run(
                AsyncPoolClaim.claim(POOL_ID, request_id="req-42", wait_ready=False)
            )
        self.assertEqual(claim.request_id, "req-42")
        self.assertEqual(bodies[0].request_id, "req-42")

    def test_claim_requires_pool_id(self):
        with self.assertRaises(ValueError):
            asyncio.run(AsyncPoolClaim.claim(""))

    def test_claim_raises_when_exhausted(self):
        calls = []

        async def claim_mock(**kwargs):
            calls.append(1)
            raise AsyncApiException(status=503, reason="Service Unavailable")

        clients = _async_clients(claim_mock)
        with (
            patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients),
            patch("asyncio.sleep"),
        ):
            with self.assertRaises(SandboxClaimError):
                asyncio.run(AsyncPoolClaim.claim(POOL_ID, wait_ready=False))
        self.assertEqual(len(calls), 3)  # _CLAIM_MAX_ATTEMPTS

    def test_claim_raises_when_service_id_missing(self):
        async def claim_mock(**kwargs):
            return AsyncPoolClaimReply(claim_id="cl-1", prewarmed=True)

        clients = _async_clients(claim_mock)
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            with self.assertRaises(SandboxClaimError):
                asyncio.run(AsyncPoolClaim.claim(POOL_ID, wait_ready=False))

    def _async_wait_claim(self) -> AsyncPoolClaim:
        return AsyncPoolClaim(
            pool_id=POOL_ID,
            claim_id="cl-1",
            service_id=SERVICE_ID,
            request_id="req-1",
            prewarmed=False,
        )

    def test_wait_ready_returns_true_on_degraded(self):
        # DEGRADED is ready for a claim; real async models
        # exercise the status-enum canonicalization.
        clients = MagicMock()
        clients.services.get_service = _async_return(
            _async_service_reply(AsyncServiceStatus.DEGRADED)
        )
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            self.assertTrue(asyncio.run(self._async_wait_claim().wait_ready(timeout=5)))

    def test_wait_ready_polls_through_404(self):
        # 404 is transient: keep polling instead of failing the
        # claim on a possibly racy lookup.
        clients = MagicMock()
        clients.services.get_service = _async_side_effect(
            [
                AsyncNotFoundException(status=404, reason="Not Found"),
                _async_service_reply(AsyncServiceStatus.HEALTHY),
            ]
        )
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            self.assertTrue(asyncio.run(self._async_wait_claim().wait_ready(timeout=5)))

    def test_wait_ready_returns_true_on_healthy(self):
        clients = MagicMock()
        clients.services.get_service = _async_return(
            _async_service_reply(AsyncServiceStatus.HEALTHY)
        )
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            self.assertTrue(asyncio.run(self._async_wait_claim().wait_ready(timeout=5)))

    def test_wait_ready_raises_on_terminal_status(self):
        clients = MagicMock()
        clients.services.get_service = _async_return(
            _async_service_reply(AsyncServiceStatus.UNHEALTHY)
        )
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            with self.assertRaises(SandboxClaimError):
                asyncio.run(self._async_wait_claim().wait_ready(timeout=5))

    def test_wait_ready_returns_false_on_timeout(self):
        clients = MagicMock()
        clients.services.get_service = _async_return(
            _async_service_reply(AsyncServiceStatus.STARTING)
        )
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            self.assertFalse(
                asyncio.run(
                    self._async_wait_claim().wait_ready(timeout=1, poll_interval=0.01)
                )
            )

    def test_wait_ready_raises_on_unclassifiable_status(self):
        # An unknown Service.Status fails deserialization before reaching the
        # classifier; fail closed fast instead of polling to timeout.
        clients = MagicMock()
        clients.services.get_service = _async_side_effect(
            [_async_status_validation_error()]
        )
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            with self.assertRaises(SandboxClaimError) as ctx:
                asyncio.run(self._async_wait_claim().wait_ready(timeout=5))
        self.assertEqual(ctx.exception.request_id, "req-1")

    def test_wait_ready_returns_false_on_persistent_errors(self):
        # Get Service failing for the whole budget is fail-closed: the claim
        # never reports ready.
        clients = MagicMock()
        clients.services.get_service = _async_raise(
            AsyncApiException(status=500, reason="Server Error")
        )
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            self.assertFalse(
                asyncio.run(
                    self._async_wait_claim().wait_ready(timeout=1, poll_interval=0.01)
                )
            )

    def test_wait_ready_stops_immediately_on_cancel_event(self):
        clients = MagicMock()
        clients.services.get_service = AsyncMock(
            return_value=_async_service_reply(AsyncServiceStatus.HEALTHY)
        )

        async def scenario() -> bool:
            # asyncio.Event binds to the running loop at construction on
            # Python 3.9, so create it inside the loop.
            cancel = asyncio.Event()
            cancel.set()
            return await self._async_wait_claim().wait_ready(timeout=5, cancel=cancel)

        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            self.assertFalse(asyncio.run(scenario()))
        self.assertEqual(clients.services.get_service.call_count, 0)

    def test_claim_raises_when_claim_id_missing(self):
        async def claim_mock(**kwargs):
            return AsyncPoolClaimReply(service_id=SERVICE_ID, prewarmed=True)

        clients = _async_clients(claim_mock)
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            with self.assertRaises(SandboxClaimError):
                asyncio.run(AsyncPoolClaim.claim(POOL_ID, wait_ready=False))

    def test_claim_prewarmed_missing_defaults_false(self):
        async def claim_mock(**kwargs):
            return AsyncPoolClaimReply(claim_id="cl-1", service_id=SERVICE_ID)

        clients = _async_clients(claim_mock)
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            claim = asyncio.run(AsyncPoolClaim.claim(POOL_ID, wait_ready=False))
        self.assertFalse(claim.prewarmed)

    def test_get_claim_fetches_claim_by_id(self):
        clients = MagicMock()
        clients.pool_claims.get_claim = AsyncMock(
            return_value=AsyncGetPoolClaimReply(claim=_async_claim_resource())
        )
        with patch("koyeb.sandbox.pool.get_async_api_clients", return_value=clients):
            resource = asyncio.run(AsyncPoolClaim.get_claim("cl-1", request_id="req-1"))
        self.assertEqual(resource.id, "cl-1")
        self.assertEqual(
            clients.pool_claims.get_claim.call_args.kwargs["claim_id"], "cl-1"
        )
        self.assertEqual(
            clients.pool_claims.get_claim.call_args.kwargs["request_id"], "req-1"
        )


def _async_return(value):
    async def call(*args, **kwargs):
        return value

    return call


def _async_side_effect(values):
    """Async callable yielding values (or raising them) in sequence."""

    async def call(*args, **kwargs):
        value = values.pop(0)
        if isinstance(value, BaseException):
            raise value
        return value

    return call


def _status_validation_error() -> ValidationError:
    """A real pydantic failure on an unknown Service.Status value."""
    try:
        GetServiceReply.model_validate(
            {"service": {"id": SERVICE_ID, "status": "TELEPORTING"}}
        )
    except ValidationError as e:
        return e
    raise AssertionError("expected a ValidationError")


def _other_field_validation_error() -> ValidationError:
    """A real pydantic failure on a non-status field."""
    try:
        GetServiceReply.model_validate(
            {
                "service": {
                    "id": SERVICE_ID,
                    "status": "HEALTHY",
                    "created_at": "not-a-date",
                }
            }
        )
    except ValidationError as e:
        return e
    raise AssertionError("expected a ValidationError")


def _async_status_validation_error() -> ValidationError:
    """A real pydantic failure on an unknown async Service.Status value."""
    try:
        AsyncGetServiceReply.model_validate(
            {"service": {"id": SERVICE_ID, "status": "TELEPORTING"}}
        )
    except ValidationError as e:
        return e
    raise AssertionError("expected a ValidationError")


def _async_raise(exc):
    async def call(*args, **kwargs):
        raise exc

    return call


class TestServiceStatusClassification(unittest.TestCase):
    """The classifier is the single source of truth for the state mapping."""

    def test_classify_all_states(self):
        expected = {
            ServiceStatus.HEALTHY: "ready",
            ServiceStatus.DEGRADED: "ready",
            ServiceStatus.STARTING: "in_progress",
            ServiceStatus.RESUMING: "in_progress",
            ServiceStatus.UNHEALTHY: "terminal",
            ServiceStatus.DELETING: "terminal",
            ServiceStatus.DELETED: "terminal",
            ServiceStatus.PAUSING: "terminal",
            ServiceStatus.PAUSED: "terminal",
        }
        self.assertEqual(set(expected), set(ServiceStatus))  # every value covered
        for status, kind in expected.items():
            self.assertEqual(_classify_service_status(status), kind)

    def test_classify_unknown_value_fails_closed(self):
        class ForwardCompatStatus(str, Enum):
            NEW = "NEW"

        self.assertEqual(_classify_service_status(ForwardCompatStatus.NEW), "terminal")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
