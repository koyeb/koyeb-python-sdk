# coding: utf-8

"""
Koyeb Service Pool - manage pools of pre-provisioned sandboxes.

A service pool keeps a target number of warm sandboxes ready so that claiming
hands out a pre-provisioned service instead of provisioning one on demand.

This module wraps the generated ServicePools API with the same ergonomics as
the rest of the sandbox layer (``Sandbox``, ``PoolClaim``): plain classes,
sync + async twins, errors in ``utils.py``, and a per-instance ``api_token`` /
``host`` so follow-up calls (``refresh``, ``update``, ``delete``) reuse the
caller's credentials.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from koyeb.api.exceptions import ApiException
from koyeb.api.models.create_service_pool import CreateServicePool
from koyeb.api.models.deployment_definition import DeploymentDefinition
from koyeb.api.models.update_service_pool import UpdateServicePool
from koyeb.api_async.exceptions import ApiException as AsyncApiException
from koyeb.api_async.models.create_service_pool import (
    CreateServicePool as AsyncCreateServicePool,
)
from koyeb.api_async.models.deployment_definition import (
    DeploymentDefinition as AsyncDeploymentDefinition,
)
from koyeb.api_async.models.update_service_pool import (
    UpdateServicePool as AsyncUpdateServicePool,
)

from .utils import (
    DEFAULT_HTTP_TIMEOUT,
    ServicePoolError,
    get_api_clients,
    get_async_api_clients,
    logger,
)

# Definition accepted as a generated model (sync or async flavor, which are
# structurally equivalent) or a dict that is upgraded to one.
DefinitionInput = Optional[
    Union[DeploymentDefinition, AsyncDeploymentDefinition, Dict[str, Any]]
]

_PoolT = TypeVar("_PoolT", bound="ServicePool")


def _normalize_definition(
    definition: DefinitionInput,
    model_cls: type,
) -> Optional[Any]:
    """Coerce a user-supplied definition into the generated model the call needs.

    A dict is upgraded to the model; an existing model is passed through
    (the sync and async flavors are structurally equivalent); None stays None.
    A malformed dict raises ``ServicePoolError`` rather than a raw pydantic
    ``ValidationError``.
    """
    if definition is None or isinstance(definition, dict):
        try:
            return model_cls(**definition) if definition else None
        except Exception as e:
            raise ServicePoolError(f"invalid deployment definition: {e}") from e
    return definition


def _api_error_detail(e: Union[ApiException, AsyncApiException]) -> str:
    """Human-readable detail from an ApiException: reason plus response body."""
    body = e.body
    if isinstance(body, bytes):
        body = body.decode("utf-8", errors="replace")
    detail = e.reason or ""
    if body:
        detail = f"{detail}: {body}" if detail else str(body)
    return detail


class ServicePool:
    """A handle on a Koyeb service pool.

    Instances are cheap value objects bound to a pool id; the classmethods
    ``create`` / ``get`` / ``list`` build them from API replies. Mutating
    methods (``update``, ``delete``, ``refresh``) reuse the ``api_token`` and
    ``host`` captured at construction.
    """

    def __init__(
        self,
        pool_id: str,
        name: Optional[str] = None,
        size: Optional[int] = None,
        definition: DefinitionInput = None,
        ready_count: Optional[int] = None,
        status: Optional[str] = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ):
        self.pool_id = pool_id
        self.name = name
        self.size = size
        self.definition = definition
        self.ready_count = ready_count
        self.status = status
        self.api_token = api_token
        self.host = host

    def __repr__(self) -> str:
        return (
            f"ServicePool(pool_id={self.pool_id!r}, name={self.name!r}, "
            f"size={self.size}, ready_count={self.ready_count}, "
            f"status={self.status!r})"
        )

    # -- construction helpers -------------------------------------------------

    @classmethod
    def _from_reply(
        cls: Type[_PoolT],
        reply: Any,
        api_token: Optional[str],
        host: Optional[str],
    ) -> _PoolT:
        pool = reply.service_pool
        if pool is None or pool.id is None:
            raise ServicePoolError("service pool reply had no service_pool.id")
        return cls(
            pool_id=pool.id,
            name=pool.name,
            size=pool.size,
            definition=pool.definition,
            ready_count=pool.ready_count,
            status=pool.status.value if pool.status is not None else None,
            api_token=api_token,
            host=host,
        )

    def _apply(self, refreshed: "ServicePool") -> None:
        """Copy mutable fields from a refreshed handle onto this one in place."""
        self.name = refreshed.name
        self.size = refreshed.size
        self.definition = refreshed.definition
        self.ready_count = refreshed.ready_count
        self.status = refreshed.status

    # -- CRUD -----------------------------------------------------------------

    @classmethod
    def create(
        cls,
        name: str,
        size: int,
        definition: DefinitionInput = None,
        *,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "ServicePool":
        """
        Create a service pool.

        Args:
            name: Human-readable name of the pool (unique per workspace).
            size: Target number of warm sandboxes to keep ready (>= 0).
            definition: Deployment definition describing the sandbox image
                the pool pre-provisions. A dict is accepted and upgraded to
                the generated ``DeploymentDefinition`` model.
            api_token: Koyeb API token (if None, reads KOYEB_API_TOKEN).
            host: Koyeb API host (if None, reads KOYEB_API_HOST; defaults to
                https://app.koyeb.com).

        Returns:
            ServicePool: The created pool.

        Raises:
            ValueError: If name or size is not provided, or size is negative.
            ServicePoolError: If the API rejects the request.

        Example:
            >>> pool = ServicePool.create("my-pool", 3,
            ...     definition={"docker": {"image": "koyeb/sandbox"}})
            >>> pool.pool_id, pool.size
            ('fd9422ce-...', 3)
        """
        if not name:
            raise ValueError("name is required")
        if size is None:
            raise ValueError("size is required")
        if size < 0:
            raise ValueError("size must not be negative")

        clients = get_api_clients(api_token, host)
        body = CreateServicePool(
            name=name,
            size=size,
            definition=_normalize_definition(definition, DeploymentDefinition),
        )
        try:
            reply = clients.service_pools.create_service_pool(
                service_pool=body, _request_timeout=DEFAULT_HTTP_TIMEOUT
            )
        except ApiException as e:
            raise ServicePoolError(
                f"Failed to create service pool '{name}': {_api_error_detail(e)}"
            ) from e
        return cls._from_reply(reply, api_token, host)

    @classmethod
    def get(
        cls,
        pool_id: str,
        *,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "ServicePool":
        """Fetch a single service pool by id.

        Args:
            pool_id: ID of the service pool to fetch.
            api_token: Koyeb API token (if None, reads KOYEB_API_TOKEN).
            host: Koyeb API host (if None, reads KOYEB_API_HOST; defaults to
                https://app.koyeb.com).

        Returns:
            ServicePool: The fetched pool.

        Raises:
            ValueError: If pool_id is not provided.
            ServicePoolError: If the API rejects the request.
        """
        if not pool_id:
            raise ValueError("pool_id is required")
        clients = get_api_clients(api_token, host)
        try:
            reply = clients.service_pools.get_service_pool(
                pool_id, _request_timeout=DEFAULT_HTTP_TIMEOUT
            )
        except ApiException as e:
            raise ServicePoolError(
                f"Failed to get service pool '{pool_id}': {_api_error_detail(e)}"
            ) from e
        return cls._from_reply(reply, api_token, host)

    @classmethod
    def list(
        cls,
        *,
        name: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> List["ServicePool"]:
        """List service pools visible to the caller (one paginated call).

        Args:
            name: Filter pools by name (case-sensitive, server-side).
            limit: Maximum number of pools to return.
            offset: Pagination offset.
            api_token: Koyeb API token (if None, reads KOYEB_API_TOKEN).
            host: Koyeb API host (if None, reads KOYEB_API_HOST; defaults to
                https://app.koyeb.com).

        Returns:
            List[ServicePool]: Pools visible to the caller. Entries without
            an id are dropped.

        Raises:
            ServicePoolError: If the API rejects the request.
        """
        clients = get_api_clients(api_token, host)
        kwargs: Dict[str, Any] = {"_request_timeout": DEFAULT_HTTP_TIMEOUT}
        if name is not None:
            kwargs["name"] = name
        if limit is not None:
            kwargs["limit"] = str(limit)
        if offset is not None:
            kwargs["offset"] = str(offset)
        try:
            reply = clients.service_pools.list_service_pools(**kwargs)
        except ApiException as e:
            raise ServicePoolError(
                f"Failed to list service pools: {_api_error_detail(e)}"
            ) from e
        pools = reply.service_pools or []
        if any(p.id is None for p in pools):
            logger.debug(
                "dropping %d service pool(s) with no id",
                sum(1 for p in pools if p.id is None),
            )
        return [
            cls(
                pool_id=p.id,
                name=p.name,
                size=p.size,
                definition=p.definition,
                ready_count=p.ready_count,
                status=p.status.value if p.status is not None else None,
                api_token=api_token,
                host=host,
            )
            for p in pools
            if p.id is not None
        ]

    def update(
        self,
        *,
        definition: DefinitionInput,
        size: Optional[int] = None,
    ) -> "ServicePool":
        """
        Replace this service pool's configuration (full PUT-replace).

        The server does not support field masks: every update replaces the
        pool's ``definition`` and, when given, ``size``. ``definition`` is
        required by the API; ``size`` defaults to the server's current value
        when omitted.

        Args:
            definition: New deployment definition (dict accepted). Required.
            size: New target number of warm sandboxes (optional, >= 0).

        Returns:
            ServicePool: self, refreshed from the reply.

        Raises:
            ValueError: If definition is not provided or size is negative.
            ServicePoolError: If the API rejects the request.
        """
        if definition is None:
            raise ValueError("definition is required")
        if size is not None and size < 0:
            raise ValueError("size must not be negative")
        clients = get_api_clients(self.api_token, self.host)
        body = UpdateServicePool(
            size=size,
            definition=_normalize_definition(definition, DeploymentDefinition),
        )
        try:
            reply = clients.service_pools.update_service_pool(
                self.pool_id,
                service_pool=body,
                _request_timeout=DEFAULT_HTTP_TIMEOUT,
            )
        except ApiException as e:
            raise ServicePoolError(
                f"Failed to update service pool '{self.pool_id}': "
                f"{_api_error_detail(e)}"
            ) from e
        self._apply(self.__class__._from_reply(reply, self.api_token, self.host))
        return self

    def delete(self) -> None:
        """Delete this service pool.

        The pool is fenced server-side until outstanding claims drain; the
        handle is stale after this.

        Raises:
            ServicePoolError: If the API rejects the request.
        """
        clients = get_api_clients(self.api_token, self.host)
        try:
            clients.service_pools.delete_service_pool(
                self.pool_id, _request_timeout=DEFAULT_HTTP_TIMEOUT
            )
        except ApiException as e:
            raise ServicePoolError(
                f"Failed to delete service pool '{self.pool_id}': "
                f"{_api_error_detail(e)}"
            ) from e

    def refresh(self) -> "ServicePool":
        """Re-fetch this pool from the API and update the handle in place.

        Returns:
            ServicePool: self, refreshed.

        Raises:
            ServicePoolError: If the API rejects the request.
        """
        clients = get_api_clients(self.api_token, self.host)
        try:
            reply = clients.service_pools.get_service_pool(
                self.pool_id, _request_timeout=DEFAULT_HTTP_TIMEOUT
            )
        except ApiException as e:
            raise ServicePoolError(
                f"Failed to refresh service pool '{self.pool_id}': "
                f"{_api_error_detail(e)}"
            ) from e
        self._apply(self.__class__._from_reply(reply, self.api_token, self.host))
        return self


class AsyncServicePool(ServicePool):
    """
    Asynchronous handle on a Koyeb service pool.

    Mirrors :class:`ServicePool` with awaitable CRUD methods.
    """

    @classmethod
    async def create(
        cls,
        name: str,
        size: int,
        definition: DefinitionInput = None,
        *,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "AsyncServicePool":
        """
        Create a service pool asynchronously.

        Args:
            name: Human-readable name of the pool (unique per workspace).
            size: Target number of warm sandboxes to keep ready (>= 0).
            definition: Deployment definition describing the sandbox image
                the pool pre-provisions. A dict is accepted and upgraded to
                the generated ``DeploymentDefinition`` model.
            api_token: Koyeb API token (if None, reads KOYEB_API_TOKEN).
            host: Koyeb API host (if None, reads KOYEB_API_HOST; defaults to
                https://app.koyeb.com).

        Returns:
            AsyncServicePool: The created pool.

        Raises:
            ValueError: If name or size is not provided, or size is negative.
            ServicePoolError: If the API rejects the request.
        """
        if not name:
            raise ValueError("name is required")
        if size is None:
            raise ValueError("size is required")
        if size < 0:
            raise ValueError("size must not be negative")
        clients = get_async_api_clients(api_token, host)
        body = AsyncCreateServicePool(
            name=name,
            size=size,
            definition=_normalize_definition(definition, AsyncDeploymentDefinition),
        )
        try:
            reply = await clients.service_pools.create_service_pool(
                service_pool=body, _request_timeout=DEFAULT_HTTP_TIMEOUT
            )
        except AsyncApiException as e:
            raise ServicePoolError(
                f"Failed to create service pool '{name}': {_api_error_detail(e)}"
            ) from e
        return cls._from_reply(reply, api_token, host)

    @classmethod
    async def get(
        cls,
        pool_id: str,
        *,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "AsyncServicePool":
        """
        Fetch a single service pool by id asynchronously.

        Args:
            pool_id: ID of the service pool to fetch.
            api_token: Koyeb API token (if None, reads KOYEB_API_TOKEN).
            host: Koyeb API host (if None, reads KOYEB_API_HOST; defaults to
                https://app.koyeb.com).

        Returns:
            AsyncServicePool: The fetched pool.

        Raises:
            ValueError: If pool_id is not provided.
            ServicePoolError: If the API rejects the request.
        """
        if not pool_id:
            raise ValueError("pool_id is required")
        clients = get_async_api_clients(api_token, host)
        try:
            reply = await clients.service_pools.get_service_pool(
                pool_id, _request_timeout=DEFAULT_HTTP_TIMEOUT
            )
        except AsyncApiException as e:
            raise ServicePoolError(
                f"Failed to get service pool '{pool_id}': {_api_error_detail(e)}"
            ) from e
        return cls._from_reply(reply, api_token, host)

    @classmethod
    async def list(
        cls,
        *,
        name: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> List["AsyncServicePool"]:
        """
        List service pools visible to the caller asynchronously.

        Args:
            name: Filter pools by name (case-sensitive, server-side).
            limit: Maximum number of pools to return.
            offset: Pagination offset.
            api_token: Koyeb API token (if None, reads KOYEB_API_TOKEN).
            host: Koyeb API host (if None, reads KOYEB_API_HOST; defaults to
                https://app.koyeb.com).

        Returns:
            List[AsyncServicePool]: Pools visible to the caller. Entries
            without an id are dropped.

        Raises:
            ServicePoolError: If the API rejects the request.
        """
        clients = get_async_api_clients(api_token, host)
        kwargs: Dict[str, Any] = {"_request_timeout": DEFAULT_HTTP_TIMEOUT}
        if name is not None:
            kwargs["name"] = name
        if limit is not None:
            kwargs["limit"] = str(limit)
        if offset is not None:
            kwargs["offset"] = str(offset)
        try:
            reply = await clients.service_pools.list_service_pools(**kwargs)
        except AsyncApiException as e:
            raise ServicePoolError(
                f"Failed to list service pools: {_api_error_detail(e)}"
            ) from e
        pools = reply.service_pools or []
        if any(p.id is None for p in pools):
            logger.debug(
                "dropping %d service pool(s) with no id",
                sum(1 for p in pools if p.id is None),
            )
        return [
            cls(
                pool_id=p.id,
                name=p.name,
                size=p.size,
                definition=p.definition,
                ready_count=p.ready_count,
                status=p.status.value if p.status is not None else None,
                api_token=api_token,
                host=host,
            )
            for p in pools
            if p.id is not None
        ]

    async def update(
        self,
        *,
        definition: DefinitionInput,
        size: Optional[int] = None,
    ) -> "AsyncServicePool":
        """
        Replace this service pool's configuration asynchronously (full PUT-replace).

        The server does not support field masks: every update replaces the
        pool's ``definition`` and, when given, ``size``. ``definition`` is
        required by the API; ``size`` defaults to the server's current value
        when omitted.

        Args:
            definition: New deployment definition (dict accepted). Required.
            size: New target number of warm sandboxes (optional, >= 0).

        Returns:
            AsyncServicePool: self, refreshed from the reply.

        Raises:
            ValueError: If definition is not provided or size is negative.
            ServicePoolError: If the API rejects the request.
        """
        if definition is None:
            raise ValueError("definition is required")
        if size is not None and size < 0:
            raise ValueError("size must not be negative")
        clients = get_async_api_clients(self.api_token, self.host)
        body = AsyncUpdateServicePool(
            size=size,
            definition=_normalize_definition(definition, AsyncDeploymentDefinition),
        )
        try:
            reply = await clients.service_pools.update_service_pool(
                self.pool_id,
                service_pool=body,
                _request_timeout=DEFAULT_HTTP_TIMEOUT,
            )
        except AsyncApiException as e:
            raise ServicePoolError(
                f"Failed to update service pool '{self.pool_id}': "
                f"{_api_error_detail(e)}"
            ) from e
        self._apply(self.__class__._from_reply(reply, self.api_token, self.host))
        return self

    async def delete(self) -> None:
        """Delete this service pool asynchronously.

        The pool is fenced server-side until outstanding claims drain; the
        handle is stale after this.

        Raises:
            ServicePoolError: If the API rejects the request.
        """
        clients = get_async_api_clients(self.api_token, self.host)
        try:
            await clients.service_pools.delete_service_pool(
                self.pool_id, _request_timeout=DEFAULT_HTTP_TIMEOUT
            )
        except AsyncApiException as e:
            raise ServicePoolError(
                f"Failed to delete service pool '{self.pool_id}': "
                f"{_api_error_detail(e)}"
            ) from e

    async def refresh(self) -> "AsyncServicePool":
        """Re-fetch this pool from the API and update the handle in place.

        Returns:
            AsyncServicePool: self, refreshed.

        Raises:
            ServicePoolError: If the API rejects the request.
        """
        clients = get_async_api_clients(self.api_token, self.host)
        try:
            reply = await clients.service_pools.get_service_pool(
                self.pool_id, _request_timeout=DEFAULT_HTTP_TIMEOUT
            )
        except AsyncApiException as e:
            raise ServicePoolError(
                f"Failed to refresh service pool '{self.pool_id}': "
                f"{_api_error_detail(e)}"
            ) from e
        self._apply(self.__class__._from_reply(reply, self.api_token, self.host))
        return self
