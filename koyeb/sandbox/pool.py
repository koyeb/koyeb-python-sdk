"""
Koyeb service pools: pre-warmed sandbox pools and claims.

Mirrors the JS SDK's service-pool.ts / claim.ts: a pool keeps ``size``
pre-warmed services ready; ``claim()`` hands one out idempotently (the
same ``request_id`` returns the same claim), retrying transient failures
(429/5xx) with linear backoff. Sync and async are fully mirrored.
"""

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass
from typing import Any, List, Optional, Union

from pydantic import ValidationError

from koyeb.api.exceptions import ApiException
from koyeb.api.models.create_service_pool import CreateServicePool
from koyeb.api.models.deployment_definition_type import DeploymentDefinitionType
from koyeb.api.models.deployment_health_check import DeploymentHealthCheck
from koyeb.api.models.deployment_port import DeploymentPort
from koyeb.api.models.deployment_proxy_port import DeploymentProxyPort
from koyeb.api.models.deployment_route import DeploymentRoute
from koyeb.api.models.deployment_volume import DeploymentVolume
from koyeb.api.models.pool_claim import PoolClaim
from koyeb.api.models.pool_claim_request import PoolClaimRequest
from koyeb.api.models.update_service_pool import UpdateServicePool
from koyeb.api_async.exceptions import ApiException as AsyncApiException
from koyeb.api_async.models.create_service_pool import (
    CreateServicePool as AsyncCreateServicePool,
)
from koyeb.api_async.models.pool_claim_request import (
    PoolClaimRequest as AsyncPoolClaimRequest,
)
from koyeb.api_async.models.update_service_pool import (
    UpdateServicePool as AsyncUpdateServicePool,
)

from .spec import SandboxSpec, build_archive_source
from .clients import get_api_clients, get_async_api_clients
from .errors import (
    PoolClaimError,
    ServicePoolError,
    ServiceTerminalStateError,
)
from .status import classify_service_status

logger = logging.getLogger(__name__)

DEFAULT_POOL_SIZE = 1
_POOL_DEFINITION_TYPES = {
    "WEB": DeploymentDefinitionType.WEB,
    "WORKER": DeploymentDefinitionType.WORKER,
    "SANDBOX": DeploymentDefinitionType.SANDBOX,
}
DEFAULT_CLAIM_ATTEMPTS = 3
DEFAULT_CLAIM_RETRY_DELAY = 1.0  # seconds; linear: delay * attempt number
DEFAULT_CLAIM_WAIT_TIMEOUT = 300.0
DEFAULT_CLAIM_POLL_INTERVAL = 2.0


@dataclass
class ClaimResult:
    """A sandbox claimed from a service pool (``service_id`` is always set).

    The claimed sandbox is detached from the pool and owned by the caller."""

    claim_id: str
    pool_id: str
    request_id: str
    service_id: str
    prewarmed: bool


def _pool_definition_type(pool_type: str) -> DeploymentDefinitionType:
    """Map a pool ``type`` string onto the API enum, fail-fast.

    DATABASE is a product-rule exclusion: pools host WEB, WORKER, and
    SANDBOX definitions only."""
    if pool_type in _POOL_DEFINITION_TYPES:
        return _POOL_DEFINITION_TYPES[pool_type]
    if pool_type == "DATABASE":
        raise ServicePoolError(
            "Invalid pool type 'DATABASE': service pools do not host "
            "DATABASE definitions (allowed: WEB, WORKER, SANDBOX)"
        )
    raise ServicePoolError(
        f"Invalid pool type {pool_type!r}: must be one of " "'WEB', 'WORKER', 'SANDBOX'"
    )


def _validate_pool_member_knobs(
    pool_type: Any,
    checks: Optional[List[Any]] = None,
    proxy_ports: Optional[List[Any]] = None,
) -> None:
    """Gate the member definition knobs on the pool type (create and
    update share the rule)."""
    if checks is not None and pool_type != "WEB":
        raise ServicePoolError(
            "checks are only allowed on WEB pools: "
            f"{pool_type} pool members do not accept health checks"
        )
    if proxy_ports is not None and pool_type == "SANDBOX":
        raise ServicePoolError(
            "proxy_ports are not allowed on SANDBOX pools: the sandbox "
            "wiring owns ports 3030/3031 — expose port 3031 with the "
            "sandbox-only enable_tcp_proxy option instead"
        )


def _validate_pool_create_args(
    pool_type: str,
    ports: Optional[List[Any]],
    routes: Optional[List[Any]],
    exposed_port_protocol: Optional[str] = None,
    enable_tcp_proxy: bool = False,
    checks: Optional[List[Any]] = None,
    proxy_ports: Optional[List[Any]] = None,
    archive: Optional[Any] = None,
    docker_source_given: bool = False,
) -> None:
    """Fail-fast on type/wiring mismatches, before any API call."""
    if pool_type == "SANDBOX" and (ports or routes):
        raise ServicePoolError(
            "SANDBOX pools do not accept explicit ports or routes: the "
            "sandbox wiring owns ports 3030/3031, and user ports would "
            "break executor connectivity"
        )
    if pool_type != "SANDBOX" and (
        exposed_port_protocol is not None or enable_tcp_proxy
    ):
        raise ServicePoolError(
            "exposed_port_protocol and enable_tcp_proxy are sandbox-only "
            f"options and cannot be used on {pool_type} pools"
        )
    _validate_pool_member_knobs(pool_type, checks, proxy_ports)
    if archive is not None and docker_source_given:
        raise ServicePoolError(
            "invalid member source: the pool member source is either a "
            "Docker image or an archive — archive cannot be combined "
            "with image or the docker overrides (entrypoint, command, "
            "args, registry_secret, privileged)"
        )


def _coerce_ports(ports: Optional[List[Any]]) -> Optional[List[DeploymentPort]]:
    """Accept DeploymentPort models or ``{port, protocol}`` dicts; verbatim."""
    if ports is None:
        return None
    return [p if isinstance(p, DeploymentPort) else DeploymentPort(**p) for p in ports]


def _coerce_routes(routes: Optional[List[Any]]) -> Optional[List[DeploymentRoute]]:
    """Accept DeploymentRoute models or ``{port, path}`` dicts; verbatim."""
    if routes is None:
        return None
    return [
        r if isinstance(r, DeploymentRoute) else DeploymentRoute(**r) for r in routes
    ]


def _coerce_checks(
    checks: Optional[List[Any]],
) -> Optional[List[DeploymentHealthCheck]]:
    """Accept DeploymentHealthCheck models or wire-shaped dicts
    (``{"http": {"port": ..., "path": ...}}``, ``{"tcp": {"port": ...}}``
    plus optional grace_period/interval/timeout/restart_limit); verbatim."""
    if checks is None:
        return None
    coerced = []
    for check in checks:
        if not isinstance(check, DeploymentHealthCheck):
            check = DeploymentHealthCheck(**check)
        if not (check.http or check.tcp or check.grpc):
            raise ServicePoolError(
                f"Invalid health check {check!r}: a check needs a probe — "
                "use the wire shape ({{'http': {{'port': ..., 'path': ...}}}} "
                "or {{'tcp': {{'port': ...}}}}) or a DeploymentHealthCheck model"
            )
        coerced.append(check)
    return coerced


def _coerce_volumes(volumes: Optional[List[Any]]) -> Optional[List[DeploymentVolume]]:
    """Accept DeploymentVolume models, ``{id, path}`` dicts, or CLI-style
    ``VOLUME:PATH`` strings (volume ids, not names: the SDK makes no
    name-resolution API call)."""
    if volumes is None:
        return None
    coerced = []
    for volume in volumes:
        if isinstance(volume, DeploymentVolume):
            coerced.append(volume)
        elif isinstance(volume, str):
            parts = volume.split(":")
            if len(parts) != 2 or not parts[0] or not parts[1]:
                raise ServicePoolError(
                    f"Invalid volume {volume!r}: volumes must be specified as "
                    "VOLUME:PATH, for example 'my-volume:/data'"
                )
            coerced.append(DeploymentVolume(id=parts[0], path=parts[1]))
        else:
            if not volume.get("id") or not volume.get("path"):
                raise ServicePoolError(
                    f"Invalid volume {volume!r}: a volume mount needs both "
                    "an 'id' and a 'path'"
                )
            coerced.append(DeploymentVolume(**volume))
    return coerced


def _coerce_proxy_ports(
    proxy_ports: Optional[List[Any]],
) -> Optional[List[DeploymentProxyPort]]:
    """Accept DeploymentProxyPort models or ``{port, protocol}`` dicts;
    protocol defaults to tcp (the API model's default)."""
    if proxy_ports is None:
        return None
    coerced = []
    for proxy_port in proxy_ports:
        if isinstance(proxy_port, DeploymentProxyPort):
            coerced.append(proxy_port)
            continue
        try:
            coerced.append(DeploymentProxyPort(**proxy_port))
        except ValidationError as e:
            raise ServicePoolError(f"Invalid proxy port {proxy_port!r}: {e}") from e
    return coerced


def _merge_member_knobs(
    definition: Any,
    checks: Optional[List[Any]] = None,
    volumes: Optional[List[Any]] = None,
    proxy_ports: Optional[List[Any]] = None,
    archive: Optional[Any] = None,
) -> Any:
    """Merge the provided member knobs over a live definition, in place
    (the update is a full replace: None keeps the live value, a provided
    knob replaces its field on the definition).

    Works on both generated model flavors: payload dicts are the wire
    truth and each flavor coerces them on assignment. The archive knob
    replaces the member source (the docker source is cleared)."""
    if all(knob is None for knob in (checks, volumes, proxy_ports, archive)):
        return definition
    if definition is None:
        raise ServicePoolError(
            "cannot update member knobs: the pool has no definition to update"
        )
    _validate_pool_member_knobs(definition.type, checks, proxy_ports)
    if checks is not None:
        definition.health_checks = [c.to_dict() for c in _coerce_checks(checks)]
    if volumes is not None:
        definition.volumes = [v.to_dict() for v in _coerce_volumes(volumes)]
    if proxy_ports is not None:
        definition.proxy_ports = [p.to_dict() for p in _coerce_proxy_ports(proxy_ports)]
    if archive is not None:
        definition.archive = build_archive_source(archive).to_dict()
        definition.docker = None
    return definition


def _claim_error_retryable(status: Any) -> bool:
    """Claims are idempotent per (pool_id, request_id): only transient
    failures (429, 5xx) are worth retrying."""
    return status == 429 or (isinstance(status, int) and status >= 500)


def claim(
    pool_id: str,
    request_id: Optional[str] = None,
    api_token: Optional[str] = None,
    host: Optional[str] = None,
    max_attempts: int = DEFAULT_CLAIM_ATTEMPTS,
    retry_delay: float = DEFAULT_CLAIM_RETRY_DELAY,
) -> ClaimResult:
    """Claim a sandbox from a service pool.

    On the warm path (``prewarmed=True``) the claimed sandbox is already
    running. On the cold path a sandbox service is created on demand:
    ``service_id`` is returned immediately and the sandbox becomes usable
    once the service is ready — see ``wait_claim_ready``.

    The claimed service is detached from the pool and owned by the
    caller: delete it like any other sandbox once you are done with it.

    Idempotent: the same ``(pool_id, request_id)`` pair always returns the
    same claim; ``request_id`` defaults to a generated UUID and is preserved
    across the SDK's internal retries.
    """
    if request_id is None:
        request_id = str(uuid.uuid4())
    clients = get_api_clients(api_token, host)

    for attempt in range(1, max_attempts + 1):
        try:
            reply = clients.pool_claims.claim(
                body=PoolClaimRequest(pool_id=pool_id, request_id=request_id)
            )
        except ApiException as e:
            if attempt >= max_attempts or not _claim_error_retryable(e.status):
                raise PoolClaimError(
                    f"Failed to claim a sandbox from pool '{pool_id}' "
                    f"(attempt {attempt}/{max_attempts}): {e}"
                ) from e
            logger.debug(
                f"Claim attempt {attempt}/{max_attempts} failed "
                f"(status {e.status}); retrying"
            )
            time.sleep(retry_delay * attempt)
            continue

        if not getattr(reply, "claim_id", None) or not getattr(
            reply, "service_id", None
        ):
            raise PoolClaimError(
                f"Pool claim reply for pool '{pool_id}' did not include "
                f"claim_id/service_id"
            )

        prewarmed = getattr(reply, "prewarmed", None)
        return ClaimResult(
            claim_id=reply.claim_id,
            pool_id=pool_id,
            request_id=request_id,
            service_id=reply.service_id,
            prewarmed=bool(prewarmed) if prewarmed is not None else False,
        )

    raise PoolClaimError(
        f"Failed to claim a sandbox from pool '{pool_id}' "
        f"after {max_attempts} attempts"
    )  # pragma: no cover - loop always returns or raises


async def claim_async(
    pool_id: str,
    request_id: Optional[str] = None,
    api_token: Optional[str] = None,
    host: Optional[str] = None,
    max_attempts: int = DEFAULT_CLAIM_ATTEMPTS,
    retry_delay: float = DEFAULT_CLAIM_RETRY_DELAY,
) -> ClaimResult:
    """Async twin of :func:`claim`."""
    if request_id is None:
        request_id = str(uuid.uuid4())
    clients = get_async_api_clients(api_token, host)

    for attempt in range(1, max_attempts + 1):
        try:
            reply = await clients.pool_claims.claim(
                body=AsyncPoolClaimRequest(pool_id=pool_id, request_id=request_id)
            )
        except AsyncApiException as e:
            if attempt >= max_attempts or not _claim_error_retryable(e.status):
                raise PoolClaimError(
                    f"Failed to claim a sandbox from pool '{pool_id}' "
                    f"(attempt {attempt}/{max_attempts}): {e}"
                ) from e
            logger.debug(
                f"Claim attempt {attempt}/{max_attempts} failed "
                f"(status {e.status}); retrying"
            )
            await asyncio.sleep(retry_delay * attempt)
            continue

        if not getattr(reply, "claim_id", None) or not getattr(
            reply, "service_id", None
        ):
            raise PoolClaimError(
                f"Pool claim reply for pool '{pool_id}' did not include "
                f"claim_id/service_id"
            )

        prewarmed = getattr(reply, "prewarmed", None)
        return ClaimResult(
            claim_id=reply.claim_id,
            pool_id=pool_id,
            request_id=request_id,
            service_id=reply.service_id,
            prewarmed=bool(prewarmed) if prewarmed is not None else False,
        )

    raise PoolClaimError(
        f"Failed to claim a sandbox from pool '{pool_id}' "
        f"after {max_attempts} attempts"
    )  # pragma: no cover - loop always returns or raises


def get_claim(
    claim_id: str,
    api_token: Optional[str] = None,
    host: Optional[str] = None,
) -> PoolClaim:
    """Fetch a claim's state (UNSPECIFIED, PENDING, FULFILLED, FAILED, RELEASED)."""
    clients = get_api_clients(api_token, host)
    return clients.pool_claims.get_claim(claim_id).claim


async def get_claim_async(
    claim_id: str,
    api_token: Optional[str] = None,
    host: Optional[str] = None,
) -> Any:
    """Async twin of :func:`get_claim`."""
    clients = get_async_api_clients(api_token, host)
    return (await clients.pool_claims.get_claim(claim_id)).claim


def list_claims(
    pool_id: str,
    status: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    api_token: Optional[str] = None,
    host: Optional[str] = None,
) -> List[PoolClaim]:
    """List claims on a service pool, optionally filtered by status."""
    clients = get_api_clients(api_token, host)
    reply = clients.pool_claims.list_claim(
        pool_id=pool_id,
        status=status,
        limit=str(limit) if limit is not None else None,
        offset=str(offset) if offset is not None else None,
    )
    return list(reply.claims or [])


async def list_claims_async(
    pool_id: str,
    status: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    api_token: Optional[str] = None,
    host: Optional[str] = None,
) -> List[Any]:
    """Async twin of :func:`list_claims`."""
    clients = get_async_api_clients(api_token, host)
    reply = await clients.pool_claims.list_claim(
        pool_id=pool_id,
        status=status,
        limit=str(limit) if limit is not None else None,
        offset=str(offset) if offset is not None else None,
    )
    return list(reply.claims or [])


def wait_claim_ready(
    claim_or_service_id: Union[ClaimResult, str],
    timeout: float = DEFAULT_CLAIM_WAIT_TIMEOUT,
    poll_interval: float = DEFAULT_CLAIM_POLL_INTERVAL,
    api_token: Optional[str] = None,
    host: Optional[str] = None,
) -> bool:
    """Poll Get Service until the claimed sandbox is ready.

    General service-health polling: returns True on ready, False on
    timeout, and raises :class:`ServiceTerminalStateError` on terminal
    states. Transient Get Service failures are treated as in-progress and
    retried until the timeout (they dominate while a cold claim provisions).
    """
    service_id = (
        claim_or_service_id.service_id
        if isinstance(claim_or_service_id, ClaimResult)
        else claim_or_service_id
    )
    clients = get_api_clients(api_token, host)
    start = time.time()

    while time.time() - start < timeout:
        status = None
        try:
            status = clients.services.get_service(service_id).service.status
        except Exception as e:
            logger.debug(f"Get Service {service_id} failed, will retry: {e}")
        if status is not None:
            classification = classify_service_status(status)
            if classification == "terminal_failure":
                raise ServiceTerminalStateError(service_id, status)
            if classification == "ready":
                return True
        time.sleep(poll_interval)

    return False


async def wait_claim_ready_async(
    claim_or_service_id: Union[ClaimResult, str],
    timeout: float = DEFAULT_CLAIM_WAIT_TIMEOUT,
    poll_interval: float = DEFAULT_CLAIM_POLL_INTERVAL,
    api_token: Optional[str] = None,
    host: Optional[str] = None,
) -> bool:
    """Async twin of :func:`wait_claim_ready`."""
    service_id = (
        claim_or_service_id.service_id
        if isinstance(claim_or_service_id, ClaimResult)
        else claim_or_service_id
    )
    clients = get_async_api_clients(api_token, host)
    start = time.time()

    while time.time() - start < timeout:
        status = None
        try:
            status = (await clients.services.get_service(service_id)).service.status
        except Exception as e:
            logger.debug(f"Get Service {service_id} failed, will retry: {e}")
        if status is not None:
            classification = classify_service_status(status)
            if classification == "terminal_failure":
                raise ServiceTerminalStateError(service_id, status)
            if classification == "ready":
                return True
        await asyncio.sleep(poll_interval)

    return False


class ServicePool:
    """A Koyeb service pool keeping pre-warmed sandboxes ready to claim."""

    def __init__(
        self,
        id: str,
        name: str,
        size: int,
        ready_count: int,
        status: Any,
        definition: Any = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.size = size
        self.ready_count = ready_count
        self.status = status
        self.definition = definition
        self.api_token = api_token
        self.host = host

    @classmethod
    def create(
        cls,
        name: str,
        image: str = "koyeb/sandbox",
        size: int = DEFAULT_POOL_SIZE,
        instance_type: str = "micro",
        region: Optional[str] = None,
        env: Optional[dict] = None,
        config_files: Optional[dict] = None,
        type: str = "SANDBOX",
        entrypoint: Optional[List[str]] = None,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        ports: Optional[List[Any]] = None,
        routes: Optional[List[Any]] = None,
        checks: Optional[List[Any]] = None,
        volumes: Optional[List[Any]] = None,
        proxy_ports: Optional[List[Any]] = None,
        archive: Optional[Any] = None,
        privileged: bool = False,
        registry_secret: Optional[str] = None,
        exposed_port_protocol: Optional[str] = None,
        enable_tcp_proxy: bool = False,
        idle_timeout: int = 300,
        _experimental_enable_light_sleep: bool = False,
        block_network: bool = False,
        outbound_allowlist: Optional[List[str]] = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "ServicePool":
        """Create a pool of ``size`` pre-warmed services built from one
        definition.

        ``type`` selects the definition type: WEB, WORKER, or SANDBOX (the
        default). SANDBOX pools keep the sandbox auto-wiring (ports 3030/3031
        and the sandbox routes); the platform mints their executor secret, and
        an explicit ``SANDBOX_SECRET`` in ``env`` wins over minting. WEB and
        WORKER pools carry exactly the declared ``ports`` and ``routes`` — no
        secret, no auto ports. The docker overrides (``entrypoint``,
        ``command``, ``args``) apply to every pool type. Mesh stays AUTO:
        there is no pool-level mesh option.

        Member definition knobs: ``checks`` (WEB pools only) are health
        checks; ``volumes`` (every pool type) are ``VOLUME:PATH`` mounts;
        ``proxy_ports`` (WEB/WORKER pools only) expose ports through the
        Koyeb proxy — SANDBOX pools expose port 3031 with the separate
        ``enable_tcp_proxy`` option instead; ``archive`` (``{"id": ...}``
        plus optional ``builder``/``buildpack``/``docker`` options) boots
        the members from an existing archive and replaces the Docker image
        source. Invalid combinations fail fast with a ``ServicePoolError``
        before any API call."""
        _validate_pool_create_args(
            type,
            ports,
            routes,
            exposed_port_protocol,
            enable_tcp_proxy,
            checks=checks,
            proxy_ports=proxy_ports,
            archive=archive,
            docker_source_given=bool(
                entrypoint
                or command
                or args
                or registry_secret
                or privileged
                or image != "koyeb/sandbox"
            ),
        )
        spec = SandboxSpec(
            name=name,
            image=image,
            instance_type=instance_type,
            definition_type=_pool_definition_type(type),
            region=region,
            env=env,
            config_files=config_files,
            entrypoint=entrypoint,
            command=command,
            args=args,
            ports=_coerce_ports(ports),
            routes=_coerce_routes(routes),
            health_checks=_coerce_checks(checks),
            volumes=_coerce_volumes(volumes),
            proxy_ports=_coerce_proxy_ports(proxy_ports),
            archive=build_archive_source(archive) if archive is not None else None,
            privileged=privileged,
            registry_secret=registry_secret,
            exposed_port_protocol=exposed_port_protocol,
            enable_tcp_proxy=enable_tcp_proxy,
            idle_timeout=idle_timeout,
            enable_light_sleep=_experimental_enable_light_sleep,
            block_network=block_network,
            outbound_allowlist=outbound_allowlist,
        )
        # The platform mints the executor secret for SANDBOX pools; mesh stays auto.
        clients = get_api_clients(api_token, host)
        try:
            reply = clients.service_pools.create_service_pool(
                service_pool=CreateServicePool(
                    name=name, size=size, definition=spec.deployment_definition()
                )
            )
        except ApiException as e:
            raise ServicePoolError(
                f"Failed to create service pool '{name}': {e}"
            ) from e
        return cls._from_model(reply.service_pool, api_token, host)

    @classmethod
    def get(
        cls,
        pool_id: str,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "ServicePool":
        clients = get_api_clients(api_token, host)
        try:
            reply = clients.service_pools.get_service_pool(pool_id)
        except ApiException as e:
            raise ServicePoolError(
                f"Failed to get service pool '{pool_id}': {e}"
            ) from e
        return cls._from_model(reply.service_pool, api_token, host)

    @classmethod
    def list(
        cls,
        name: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> List["ServicePool"]:
        clients = get_api_clients(api_token, host)
        try:
            reply = clients.service_pools.list_service_pools(
                name=name,
                limit=str(limit) if limit is not None else None,
                offset=str(offset) if offset is not None else None,
            )
        except ApiException as e:
            raise ServicePoolError(f"Failed to list service pools: {e}") from e
        return [
            cls._from_model(pool, api_token, host) for pool in reply.service_pools or []
        ]

    def update(
        self,
        size: Optional[int] = None,
        checks: Optional[List[Any]] = None,
        volumes: Optional[List[Any]] = None,
        proxy_ports: Optional[List[Any]] = None,
        archive: Optional[Any] = None,
    ) -> "ServicePool":
        """Resize the pool and/or update its member definition knobs
        (checks, volumes, proxy_ports, archive); returns the updated pool.

        Every knob is optional: None keeps the live value, so ``update(size=n)``
        stays the minimal working path. A provided knob replaces its field on
        the live definition before the resend."""
        clients = get_api_clients(self.api_token, self.host)
        try:
            # The update endpoint is a full replace: refetch the live pool so
            # the resend carries the current definition, not a stale cache.
            current = clients.service_pools.get_service_pool(self.id).service_pool
            definition = _merge_member_knobs(
                current.definition, checks, volumes, proxy_ports, archive
            )
            reply = clients.service_pools.update_service_pool(
                id=self.id,
                service_pool=UpdateServicePool(
                    size=current.size if size is None else size,
                    definition=definition,
                ),
            )
        except ApiException as e:
            raise ServicePoolError(
                f"Failed to update service pool '{self.id}': {e}"
            ) from e
        return ServicePool._from_model(reply.service_pool, self.api_token, self.host)

    def delete(self) -> None:
        """Delete the pool (async server-side: it enters DELETING)."""
        clients = get_api_clients(self.api_token, self.host)
        try:
            clients.service_pools.delete_service_pool(self.id)
        except ApiException as e:
            raise ServicePoolError(
                f"Failed to delete service pool '{self.id}': {e}"
            ) from e

    def refresh(self) -> "ServicePool":
        """Re-fetch the pool's state (ready_count, status) in place."""
        clients = get_api_clients(self.api_token, self.host)
        try:
            reply = clients.service_pools.get_service_pool(self.id)
        except ApiException as e:
            raise ServicePoolError(
                f"Failed to refresh service pool '{self.id}': {e}"
            ) from e
        model = reply.service_pool
        self.name = model.name
        self.size = model.size
        self.ready_count = model.ready_count
        self.status = model.status
        self.definition = model.definition
        return self

    def claims(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[PoolClaim]:
        return list_claims(
            self.id,
            status=status,
            limit=limit,
            offset=offset,
            api_token=self.api_token,
            host=self.host,
        )

    @staticmethod
    def _from_model(
        model: Any,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "ServicePool":
        return ServicePool(
            id=model.id,
            name=model.name,
            size=model.size,
            ready_count=model.ready_count,
            status=model.status,
            definition=model.definition,
            api_token=api_token,
            host=host,
        )


class AsyncServicePool:
    """Async twin of :class:`ServicePool`."""

    def __init__(
        self,
        id: str,
        name: str,
        size: int,
        ready_count: int,
        status: Any,
        definition: Any = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.size = size
        self.ready_count = ready_count
        self.status = status
        self.definition = definition
        self.api_token = api_token
        self.host = host

    @classmethod
    async def create(
        cls,
        name: str,
        image: str = "koyeb/sandbox",
        size: int = DEFAULT_POOL_SIZE,
        instance_type: str = "micro",
        region: Optional[str] = None,
        env: Optional[dict] = None,
        config_files: Optional[dict] = None,
        type: str = "SANDBOX",
        entrypoint: Optional[List[str]] = None,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        ports: Optional[List[Any]] = None,
        routes: Optional[List[Any]] = None,
        checks: Optional[List[Any]] = None,
        volumes: Optional[List[Any]] = None,
        proxy_ports: Optional[List[Any]] = None,
        archive: Optional[Any] = None,
        privileged: bool = False,
        registry_secret: Optional[str] = None,
        exposed_port_protocol: Optional[str] = None,
        enable_tcp_proxy: bool = False,
        idle_timeout: int = 300,
        _experimental_enable_light_sleep: bool = False,
        block_network: bool = False,
        outbound_allowlist: Optional[List[str]] = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "AsyncServicePool":
        _validate_pool_create_args(
            type,
            ports,
            routes,
            exposed_port_protocol,
            enable_tcp_proxy,
            checks=checks,
            proxy_ports=proxy_ports,
            archive=archive,
            docker_source_given=bool(
                entrypoint
                or command
                or args
                or registry_secret
                or privileged
                or image != "koyeb/sandbox"
            ),
        )
        spec = SandboxSpec(
            name=name,
            image=image,
            instance_type=instance_type,
            definition_type=_pool_definition_type(type),
            region=region,
            env=env,
            config_files=config_files,
            entrypoint=entrypoint,
            command=command,
            args=args,
            ports=_coerce_ports(ports),
            routes=_coerce_routes(routes),
            health_checks=_coerce_checks(checks),
            volumes=_coerce_volumes(volumes),
            proxy_ports=_coerce_proxy_ports(proxy_ports),
            archive=build_archive_source(archive) if archive is not None else None,
            privileged=privileged,
            registry_secret=registry_secret,
            exposed_port_protocol=exposed_port_protocol,
            enable_tcp_proxy=enable_tcp_proxy,
            idle_timeout=idle_timeout,
            enable_light_sleep=_experimental_enable_light_sleep,
            block_network=block_network,
            outbound_allowlist=outbound_allowlist,
        )
        # The platform mints the executor secret for SANDBOX pools; mesh stays auto.
        clients = get_async_api_clients(api_token, host)
        try:
            reply = await clients.service_pools.create_service_pool(
                service_pool=AsyncCreateServicePool(
                    name=name, size=size, definition=spec.deployment_definition_dict()
                )
            )
        except AsyncApiException as e:
            raise ServicePoolError(
                f"Failed to create service pool '{name}': {e}"
            ) from e
        return cls._from_model(reply.service_pool, api_token, host)

    @classmethod
    async def get(
        cls,
        pool_id: str,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "AsyncServicePool":
        clients = get_async_api_clients(api_token, host)
        try:
            reply = await clients.service_pools.get_service_pool(pool_id)
        except AsyncApiException as e:
            raise ServicePoolError(
                f"Failed to get service pool '{pool_id}': {e}"
            ) from e
        return cls._from_model(reply.service_pool, api_token, host)

    @classmethod
    async def list(
        cls,
        name: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> List["AsyncServicePool"]:
        clients = get_async_api_clients(api_token, host)
        try:
            reply = await clients.service_pools.list_service_pools(
                name=name,
                limit=str(limit) if limit is not None else None,
                offset=str(offset) if offset is not None else None,
            )
        except AsyncApiException as e:
            raise ServicePoolError(f"Failed to list service pools: {e}") from e
        return [
            cls._from_model(pool, api_token, host) for pool in reply.service_pools or []
        ]

    async def update(
        self,
        size: Optional[int] = None,
        checks: Optional[List[Any]] = None,
        volumes: Optional[List[Any]] = None,
        proxy_ports: Optional[List[Any]] = None,
        archive: Optional[Any] = None,
    ) -> "AsyncServicePool":
        """Resize the pool and/or update its member definition knobs
        (checks, volumes, proxy_ports, archive); returns the updated pool.

        Every knob is optional: None keeps the live value, so ``update(size=n)``
        stays the minimal working path. A provided knob replaces its field on
        the live definition before the resend."""
        clients = get_async_api_clients(self.api_token, self.host)
        try:
            # The update endpoint is a full replace: refetch the live pool so
            # the resend carries the current definition, not a stale cache.
            current = (
                await clients.service_pools.get_service_pool(self.id)
            ).service_pool
            definition = _merge_member_knobs(
                current.definition, checks, volumes, proxy_ports, archive
            )
            reply = await clients.service_pools.update_service_pool(
                id=self.id,
                service_pool=AsyncUpdateServicePool(
                    size=current.size if size is None else size,
                    definition=definition,
                ),
            )
        except AsyncApiException as e:
            raise ServicePoolError(
                f"Failed to update service pool '{self.id}': {e}"
            ) from e
        return AsyncServicePool._from_model(
            reply.service_pool, self.api_token, self.host
        )

    async def delete(self) -> None:
        clients = get_async_api_clients(self.api_token, self.host)
        try:
            await clients.service_pools.delete_service_pool(self.id)
        except AsyncApiException as e:
            raise ServicePoolError(
                f"Failed to delete service pool '{self.id}': {e}"
            ) from e

    async def refresh(self) -> "AsyncServicePool":
        clients = get_async_api_clients(self.api_token, self.host)
        try:
            reply = await clients.service_pools.get_service_pool(self.id)
        except AsyncApiException as e:
            raise ServicePoolError(
                f"Failed to refresh service pool '{self.id}': {e}"
            ) from e
        model = reply.service_pool
        self.name = model.name
        self.size = model.size
        self.ready_count = model.ready_count
        self.status = model.status
        self.definition = model.definition
        return self

    async def claims(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Any]:
        return await list_claims_async(
            self.id,
            status=status,
            limit=limit,
            offset=offset,
            api_token=self.api_token,
            host=self.host,
        )

    @staticmethod
    def _from_model(
        model: Any,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "AsyncServicePool":
        return AsyncServicePool(
            id=model.id,
            name=model.name,
            size=model.size,
            ready_count=model.ready_count,
            status=model.status,
            definition=model.definition,
            api_token=api_token,
            host=host,
        )
