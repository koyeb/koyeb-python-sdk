# coding: utf-8

"""
Koyeb Sandbox Pool Claim - claim pre-provisioned sandboxes from service pools.

Claiming hands out a sandbox from a pool of pre-provisioned services. When a
warm service is available the claim is fulfilled immediately (``prewarmed`` is
True); on the cold path the claimed service is still provisioning and must be
waited on before use.

Service status mapping for the cold path:

- HEALTHY, DEGRADED -> ready
- STARTING, RESUMING -> in progress (keep polling)
- UNHEALTHY (claim-flow policy), DELETING, DELETED, PAUSING, PAUSED, and any
  unknown/forward-compat value -> terminal failure (fail-closed; a status the
  SDK cannot classify fails closed the same way)
- Get Service errors, including 404, are treated as transient: keep polling
  until the timeout
"""

from __future__ import annotations

import asyncio
import secrets
import threading
import time
from typing import Literal, Optional, Union

import httpx
import urllib3
from pydantic import ValidationError

from koyeb.api.exceptions import ApiException
from koyeb.api.models.pool_claim import PoolClaim as ClaimResource
from koyeb.api.models.pool_claim_request import PoolClaimRequest
from koyeb.api.models.service_status import ServiceStatus
from koyeb.api_async.exceptions import (
    ApiException as AsyncApiException,
)
from koyeb.api_async.models.pool_claim import PoolClaim as AsyncClaimResource
from koyeb.api_async.models.pool_claim_request import (
    PoolClaimRequest as AsyncPoolClaimRequest,
)

from .utils import (
    DEFAULT_HTTP_TIMEOUT,
    DEFAULT_INSTANCE_WAIT_TIMEOUT,
    DEFAULT_POLL_INTERVAL,
    SandboxClaimError,
    SandboxTimeoutError,
    get_api_clients,
    get_async_api_clients,
    logger,
)

# The claim endpoint is idempotent per (pool_id, request_id), so replaying the
# same request after a transient failure is safe.
_RETRYABLE_STATUSES = frozenset({408, 429, 500, 502, 503, 504})

# Number of attempts for the claim call before giving up, and the delay
# between attempts (doubling up to the cap).
_CLAIM_MAX_ATTEMPTS = 3
_CLAIM_RETRY_BASE_DELAY = 0.5
_CLAIM_RETRY_MAX_DELAY = 5.0

# A cold-path claim provisions a service on demand, which can take as long
# as a fresh sandbox; budget the wait like Sandbox.create.
_CLAIM_WAIT_TIMEOUT = 300

# Exponential poll backoff seed for wait_ready (doubles up to poll_interval).
_WAIT_BACKOFF_START = 0.1

# Service states that mean "ready, use it". DEGRADED is usable for a claim:
# its active deployment is healthy and serving traffic; callers that need a
# pristine state can check status == HEALTHY themselves.
_SERVICE_READY_STATES = frozenset({ServiceStatus.HEALTHY, ServiceStatus.DEGRADED})
# States that mean "not ready yet, keep polling".
_SERVICE_IN_PROGRESS_STATES = frozenset(
    {ServiceStatus.STARTING, ServiceStatus.RESUMING}
)
# Everything else — UNHEALTHY (claim-flow policy: fail fast instead of
# polling a service that may never recover), DELETING, DELETED, PAUSING,
# PAUSED, and any unknown/forward-compat value — is terminal (fail-closed).


def _classify_service_status(
    status: ServiceStatus,
) -> Literal["ready", "in_progress", "terminal"]:
    """Classify a Service.Status for the cold-path claim poll."""
    if status in _SERVICE_READY_STATES:
        return "ready"
    if status in _SERVICE_IN_PROGRESS_STATES:
        return "in_progress"
    return "terminal"


def _is_status_field_error(e: ValidationError) -> bool:
    """True when pydantic rejected the Service.Status field itself (an
    unknown/forward-compat enum value) rather than some other field."""
    return any("status" in err.get("loc", ()) for err in e.errors())


def _new_request_id() -> str:
    """Generate a request id usable as a claim idempotency key."""
    return secrets.token_urlsafe(16)


def _api_error_detail(e: Union[ApiException, AsyncApiException]) -> str:
    """Human-readable detail from an ApiException: reason plus response body."""
    body = e.body
    if isinstance(body, bytes):
        body = body.decode("utf-8", errors="replace")
    detail = e.reason or ""
    if body:
        detail = f"{detail}: {body}" if detail else str(body)
    return detail


def _claim_failed_error(
    pool_id: str, request_id: str, e: Union[ApiException, AsyncApiException]
) -> SandboxClaimError:
    """Non-retryable claim failure: surface the HTTP error immediately."""
    return SandboxClaimError(
        f"Failed to claim from pool '{pool_id}' with request_id "
        f"'{request_id}' (HTTP {e.status}): {_api_error_detail(e)}",
        request_id=request_id,
    )


def _claim_exhausted_error(
    pool_id: str,
    request_id: str,
    attempts: int,
    last_error: Optional[BaseException],
) -> SandboxClaimError:
    """Every claim attempt failed: surface the last error with its cause."""
    detail = str(last_error) if last_error is not None else "no error recorded"
    return SandboxClaimError(
        f"Failed to claim from pool '{pool_id}' with request_id "
        f"'{request_id}' after {attempts} attempts: {detail}",
        request_id=request_id,
    )


def _claim_missing_field_error(
    pool_id: str, request_id: str, field: str
) -> SandboxClaimError:
    """Malformed claim reply: a contract-required field is absent."""
    return SandboxClaimError(
        f"Claim from pool '{pool_id}' with request_id '{request_id}' "
        f"returned no {field}",
        request_id=request_id,
    )


def _wait_timeout_error(
    service_id: str, pool_id: str, request_id: str, timeout: int
) -> SandboxTimeoutError:
    """The claimed service did not become ready within the budget."""
    return SandboxTimeoutError(
        f"Claimed service '{service_id}' from pool '{pool_id}' with "
        f"request_id '{request_id}' did not become ready within {timeout} "
        f"seconds. The claim succeeded but the service may still be "
        f"provisioning. To recover, claim again with the same request_id and "
        f"wait_ready=False, then call wait_ready()."
    )


class PoolClaim:
    """
    A claim on a sandbox from a Koyeb service pool.

    Synchronous entry point for the pool claim workflow. Use
    :class:`AsyncPoolClaim` for the async variant.

    The claim API is idempotent per ``(pool_id, request_id)``: replaying a
    claim with the same pair returns the same claim instead of consuming
    another sandbox.
    """

    def __init__(
        self,
        pool_id: str,
        service_id: str,
        request_id: str,
        prewarmed: bool,
        claim_id: Optional[str] = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ):
        self.pool_id = pool_id
        self.claim_id = claim_id
        self.service_id = service_id
        self.request_id = request_id
        self.prewarmed = prewarmed
        self.api_token = api_token
        self.host = host
        self.poll_interval = poll_interval

    def __repr__(self) -> str:
        return (
            f"PoolClaim(pool_id={self.pool_id!r}, claim_id={self.claim_id!r}, "
            f"service_id={self.service_id!r}, request_id={self.request_id!r}, "
            f"prewarmed={self.prewarmed})"
        )

    @classmethod
    def claim(
        cls,
        pool_id: str,
        request_id: Optional[str] = None,
        wait_ready: bool = True,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
        timeout: int = _CLAIM_WAIT_TIMEOUT,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> PoolClaim:
        """
        Claim a sandbox from a service pool.

        If ``request_id`` is not provided, one is generated once and reused
        for every internal retry, so a retried claim never consumes a second
        sandbox. Calling ``claim`` again with the same ``(pool_id,
        request_id)`` replays the same claim.

        Args:
            pool_id: ID of the service pool to claim from
            request_id: Idempotency key for the claim. If not provided (None
                or empty), a random one is generated. Reuse the same value to
                replay a claim.
            wait_ready: Wait for the claimed service to become ready
                (default: True). Warm claims confirm on the first poll;
                cold claims poll until ready or ``timeout`` expires.
            api_token: Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
            host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)
            timeout: Maximum time to wait for the claimed service to become
                ready when wait_ready is True (default: 300 seconds — a
                cold-path claim provisions a service on demand, so budget
                like Sandbox.create)
            poll_interval: Maximum time between status polls in seconds when
                wait_ready is True (default: 0.5)

        Returns:
            PoolClaim: The fulfilled claim. ``claim_id``, ``service_id`` and
            ``prewarmed`` are always set.

        Raises:
            ValueError: If pool_id is not provided, poll_interval is not
                greater than 0, or no API token is configured
            SandboxClaimError: If the claim fails, or the claimed service
                reaches a terminal state while waiting
            SandboxTimeoutError: If wait_ready is True and the claimed service
                does not become ready within timeout

        Example:
            >>> claim = PoolClaim.claim(pool_id="my-pool-id")
            >>> claim.service_id, claim.prewarmed
            ('fd9422ce-...', True)
            >>> # Replay the same claim (e.g. after a crash): same pair, same sandbox
            >>> claim = PoolClaim.claim(pool_id="my-pool-id", request_id=claim.request_id)
        """
        if not pool_id:
            raise ValueError("pool_id is required")
        if poll_interval <= 0:
            raise ValueError("poll_interval must be greater than 0")
        if not request_id:
            request_id = _new_request_id()

        clients = get_api_clients(api_token, host)
        body = PoolClaimRequest(pool_id=pool_id, request_id=request_id)

        reply = None
        last_error: Optional[BaseException] = None
        for attempt in range(_CLAIM_MAX_ATTEMPTS):
            try:
                reply = clients.pool_claims.claim(
                    body=body, _request_timeout=DEFAULT_HTTP_TIMEOUT
                )
                break
            except ApiException as e:
                last_error = e
                if e.status not in _RETRYABLE_STATUSES:
                    raise _claim_failed_error(pool_id, request_id, e) from e
            except urllib3.exceptions.HTTPError as e:
                # Transport-level failure (connection error, timeout, DNS):
                # replay the same request, the API deduplicates on request_id.
                last_error = e
            if attempt < _CLAIM_MAX_ATTEMPTS - 1:
                delay = min(
                    _CLAIM_RETRY_BASE_DELAY * (2**attempt), _CLAIM_RETRY_MAX_DELAY
                )
                time.sleep(delay)

        if reply is None:
            raise _claim_exhausted_error(
                pool_id, request_id, _CLAIM_MAX_ATTEMPTS, last_error
            ) from last_error

        if not reply.claim_id:
            raise _claim_missing_field_error(pool_id, request_id, "claim_id")
        service_id = reply.service_id
        if not service_id:
            raise _claim_missing_field_error(pool_id, request_id, "service_id")

        claim = cls(
            pool_id=pool_id,
            claim_id=reply.claim_id,
            service_id=service_id,
            request_id=request_id,
            prewarmed=bool(reply.prewarmed),
            api_token=api_token,
            host=host,
            poll_interval=poll_interval,
        )

        if wait_ready:
            if not claim.wait_ready(timeout=timeout):
                raise _wait_timeout_error(service_id, pool_id, request_id, timeout)
        return claim

    @classmethod
    def get_claim(
        cls,
        claim_id: str,
        request_id: Optional[str] = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> ClaimResource:
        """
        Fetch a claim's current state by id.

        Args:
            claim_id: ID of the claim to fetch
            request_id: The claim's original request id, the optional lookup
                key the claim API uses to disambiguate replayed claims
            api_token: Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
            host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)

        Returns:
            The claim resource: ``id``, ``pool_id``, ``service_id``,
            ``request_id``, ``status`` (PENDING, FULFILLED, FAILED or
            RELEASED) and timestamps.

        Raises:
            ValueError: If claim_id is not provided or no API token is
                configured
            SandboxClaimError: If the reply carries no claim resource
        """
        if not claim_id:
            raise ValueError("claim_id is required")
        clients = get_api_clients(api_token, host)
        reply = clients.pool_claims.get_claim(
            claim_id=claim_id,
            request_id=request_id,
            _request_timeout=DEFAULT_HTTP_TIMEOUT,
        )
        if reply.claim is None:
            raise SandboxClaimError(f"Get claim '{claim_id}' returned no claim")
        return reply.claim

    def wait_ready(
        self,
        timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
        poll_interval: Optional[float] = None,
        cancel: Optional[threading.Event] = None,
    ) -> bool:
        """
        Wait for the claimed service to become ready.

        Cold-path polling helper: polls Get Service with exponential backoff
        until the service is ready (HEALTHY or DEGRADED), reaches a terminal
        state (UNHEALTHY, DELETING, DELETED, PAUSING, PAUSED, or an unknown
        value — fail-closed) or the timeout expires. Warm claims are usually
        confirmed on the first poll. Transient Get Service errors, including
        404, keep polling until the timeout. A set ``cancel`` event stops
        waiting early.

        Args:
            timeout: Maximum time to wait in seconds (default: 60, the
                instance-wait budget; claim() passes its own 300s cold-path
                budget)
            poll_interval: Maximum time between status polls in seconds
                (defaults to this claim's poll_interval)
            cancel: Event that stops waiting when set; an already-set event
                returns False immediately without polling

        Returns:
            bool: True if the service became ready, False if timeout or
            cancelled

        Raises:
            ValueError: If poll_interval is not greater than 0
            SandboxClaimError: If the service reaches a terminal state,
                including a status the SDK cannot classify
        """
        if poll_interval is None:
            poll_interval = self.poll_interval
        if poll_interval <= 0:
            raise ValueError("poll_interval must be greater than 0")
        start_time = time.time()
        current_interval = _WAIT_BACKOFF_START

        while time.time() - start_time < timeout:
            if cancel is not None and cancel.is_set():
                return False
            status = self._service_status()
            if status is not None:
                kind = _classify_service_status(status)
                if kind == "ready":
                    return True
                if kind == "terminal":
                    raise SandboxClaimError(
                        f"Claimed service '{self.service_id}' reached terminal "
                        f"status {status.value}. The sandbox will not become ready.",
                        request_id=self.request_id,
                    )
            time.sleep(current_interval)
            current_interval = min(current_interval * 2, poll_interval)

        return False

    def _service_status(self) -> Optional[ServiceStatus]:
        """Fetch the claimed service's status via Get Service.

        Errors — including 404 — are treated as transient: None is returned so
        polling can continue until the timeout. An unknown Service.Status
        fails deserialization before reaching the classifier and fails closed.
        """
        try:
            clients = get_api_clients(self.api_token, self.host)
            response = clients.services.get_service(
                self.service_id, _request_timeout=DEFAULT_HTTP_TIMEOUT
            )
            service = response.service
            return service.status if service else None
        except ValidationError as e:
            if _is_status_field_error(e):
                raise SandboxClaimError(
                    f"Claimed service '{self.service_id}' returned an unknown "
                    f"service status (fail-closed): {e}",
                    request_id=self.request_id,
                ) from e
            logger.debug(f"Could not get service {self.service_id}: {e}")
            return None
        except Exception as e:
            logger.debug(f"Could not get service {self.service_id}: {e}")
            return None


class AsyncPoolClaim(PoolClaim):
    """
    Asynchronous claim on a sandbox from a Koyeb service pool.

    Mirrors :class:`PoolClaim` with awaitable ``claim`` and ``wait_ready``.
    """

    @classmethod
    async def claim(
        cls,
        pool_id: str,
        request_id: Optional[str] = None,
        wait_ready: bool = True,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
        timeout: int = _CLAIM_WAIT_TIMEOUT,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> AsyncPoolClaim:
        """
        Claim a sandbox from a service pool asynchronously.

        If ``request_id`` is not provided, one is generated once and reused
        for every internal retry, so a retried claim never consumes a second
        sandbox. Calling ``claim`` again with the same ``(pool_id,
        request_id)`` replays the same claim.

        Args:
            pool_id: ID of the service pool to claim from
            request_id: Idempotency key for the claim. If not provided (None
                or empty), a random one is generated. Reuse the same value to
                replay a claim.
            wait_ready: Wait for the claimed service to become ready
                (default: True). Warm claims confirm on the first poll;
                cold claims poll until ready or ``timeout`` expires.
            api_token: Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
            host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)
            timeout: Maximum time to wait for the claimed service to become
                ready when wait_ready is True (default: 300 seconds — a
                cold-path claim provisions a service on demand, so budget
                like Sandbox.create)
            poll_interval: Maximum time between status polls in seconds when
                wait_ready is True (default: 0.5)

        Returns:
            AsyncPoolClaim: The fulfilled claim. ``claim_id``, ``service_id``
            and ``prewarmed`` are always set.

        Raises:
            ValueError: If pool_id is not provided, poll_interval is not
                greater than 0, or no API token is configured
            SandboxClaimError: If the claim fails, or the claimed service
                reaches a terminal state while waiting
            SandboxTimeoutError: If wait_ready is True and the claimed service
                does not become ready within timeout

        Example:
            >>> claim = await AsyncPoolClaim.claim(pool_id="my-pool-id")
            >>> claim.service_id, claim.prewarmed
            ('fd9422ce-...', True)
        """
        if not pool_id:
            raise ValueError("pool_id is required")
        if poll_interval <= 0:
            raise ValueError("poll_interval must be greater than 0")
        if not request_id:
            request_id = _new_request_id()

        clients = get_async_api_clients(api_token, host)
        body = AsyncPoolClaimRequest(pool_id=pool_id, request_id=request_id)

        reply = None
        last_error: Optional[BaseException] = None
        for attempt in range(_CLAIM_MAX_ATTEMPTS):
            try:
                reply = await clients.pool_claims.claim(
                    body=body, _request_timeout=DEFAULT_HTTP_TIMEOUT
                )
                break
            except AsyncApiException as e:
                last_error = e
                if e.status not in _RETRYABLE_STATUSES:
                    raise _claim_failed_error(pool_id, request_id, e) from e
            except httpx.HTTPError as e:
                # Transport-level failure (connection error, timeout, DNS):
                # replay the same request, the API deduplicates on request_id.
                last_error = e
            if attempt < _CLAIM_MAX_ATTEMPTS - 1:
                delay = min(
                    _CLAIM_RETRY_BASE_DELAY * (2**attempt), _CLAIM_RETRY_MAX_DELAY
                )
                await asyncio.sleep(delay)

        if reply is None:
            raise _claim_exhausted_error(
                pool_id, request_id, _CLAIM_MAX_ATTEMPTS, last_error
            ) from last_error

        if not reply.claim_id:
            raise _claim_missing_field_error(pool_id, request_id, "claim_id")
        service_id = reply.service_id
        if not service_id:
            raise _claim_missing_field_error(pool_id, request_id, "service_id")

        claim = cls(
            pool_id=pool_id,
            claim_id=reply.claim_id,
            service_id=service_id,
            request_id=request_id,
            prewarmed=bool(reply.prewarmed),
            api_token=api_token,
            host=host,
            poll_interval=poll_interval,
        )

        if wait_ready:
            if not await claim.wait_ready(timeout=timeout):
                raise _wait_timeout_error(service_id, pool_id, request_id, timeout)
        return claim

    @classmethod
    async def get_claim(
        cls,
        claim_id: str,
        request_id: Optional[str] = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> AsyncClaimResource:
        """
        Fetch a claim's current state by id asynchronously.

        Args:
            claim_id: ID of the claim to fetch
            request_id: The claim's original request id, the optional lookup
                key the claim API uses to disambiguate replayed claims
            api_token: Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
            host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)

        Returns:
            The claim resource: ``id``, ``pool_id``, ``service_id``,
            ``request_id``, ``status`` (PENDING, FULFILLED, FAILED or
            RELEASED) and timestamps.

        Raises:
            ValueError: If claim_id is not provided or no API token is
                configured
            SandboxClaimError: If the reply carries no claim resource
        """
        if not claim_id:
            raise ValueError("claim_id is required")
        clients = get_async_api_clients(api_token, host)
        reply = await clients.pool_claims.get_claim(
            claim_id=claim_id,
            request_id=request_id,
            _request_timeout=DEFAULT_HTTP_TIMEOUT,
        )
        if reply.claim is None:
            raise SandboxClaimError(f"Get claim '{claim_id}' returned no claim")
        return reply.claim

    async def wait_ready(
        self,
        timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
        poll_interval: Optional[float] = None,
        cancel: Optional[asyncio.Event] = None,
    ) -> bool:
        """
        Wait for the claimed service to become ready asynchronously.

        Cold-path polling helper: polls Get Service with exponential backoff
        until the service is ready (HEALTHY or DEGRADED), reaches a terminal
        state (UNHEALTHY, DELETING, DELETED, PAUSING, PAUSED, or an unknown
        value — fail-closed) or the timeout expires. Warm claims are usually
        confirmed on the first poll. Transient Get Service errors, including
        404, keep polling until the timeout. A set ``cancel`` event stops
        waiting early, and cancelling the asyncio task stops it as well.

        Args:
            timeout: Maximum time to wait in seconds (default: 60, the
                instance-wait budget; claim() passes its own 300s cold-path
                budget)
            poll_interval: Maximum time between status polls in seconds
                (defaults to this claim's poll_interval)
            cancel: Event that stops waiting when set; an already-set event
                returns False immediately without polling

        Returns:
            bool: True if the service became ready, False if timeout or
            cancelled

        Raises:
            ValueError: If poll_interval is not greater than 0
            SandboxClaimError: If the service reaches a terminal state,
                including a status the SDK cannot classify
        """
        if poll_interval is None:
            poll_interval = self.poll_interval
        if poll_interval <= 0:
            raise ValueError("poll_interval must be greater than 0")
        start_time = time.time()
        current_interval = _WAIT_BACKOFF_START

        while time.time() - start_time < timeout:
            if cancel is not None and cancel.is_set():
                return False
            status = await self._service_status()
            if status is not None:
                kind = _classify_service_status(status)
                if kind == "ready":
                    return True
                if kind == "terminal":
                    raise SandboxClaimError(
                        f"Claimed service '{self.service_id}' reached terminal "
                        f"status {status.value}. The sandbox will not become ready.",
                        request_id=self.request_id,
                    )
            await asyncio.sleep(current_interval)
            current_interval = min(current_interval * 2, poll_interval)

        return False

    async def _service_status(self) -> Optional[ServiceStatus]:
        """Fetch the claimed service's status via Get Service.

        The async client's status enum is canonicalized to the sync one used
        for the classification. Errors — including 404 — are treated as
        transient: None is returned so polling can continue until the
        timeout. An unknown Service.Status fails deserialization before
        reaching the classifier and fails closed.
        """
        try:
            clients = get_async_api_clients(self.api_token, self.host)
            response = await clients.services.get_service(
                self.service_id, _request_timeout=DEFAULT_HTTP_TIMEOUT
            )
            service = response.service
            if service and service.status is not None:
                return ServiceStatus(service.status.value)
            return None
        except ValidationError as e:
            if _is_status_field_error(e):
                raise SandboxClaimError(
                    f"Claimed service '{self.service_id}' returned an unknown "
                    f"service status (fail-closed): {e}",
                    request_id=self.request_id,
                ) from e
            logger.debug(f"Could not get service {self.service_id}: {e}")
            return None
        except Exception as e:
            logger.debug(f"Could not get service {self.service_id}: {e}")
            return None
