import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from koyeb.api.exceptions import ApiException
from koyeb.api_async.exceptions import ApiException as AsyncApiException
from koyeb.api.models.create_service_pool_reply import CreateServicePoolReply
from koyeb.api.models.deployment_definition import DeploymentDefinition
from koyeb.api.models.get_service_pool_reply import GetServicePoolReply
from koyeb.api.models.list_service_pools_reply import ListServicePoolsReply
from koyeb.api.models.service_pool import ServicePool as ServicePoolModel
from koyeb.api.models.service_pool_status import ServicePoolStatus
from koyeb.api.models.update_service_pool_reply import UpdateServicePoolReply
from koyeb.api_async.models.create_service_pool_reply import (
    CreateServicePoolReply as AsyncCreateServicePoolReply,
)
from koyeb.api_async.models.get_service_pool_reply import (
    GetServicePoolReply as AsyncGetServicePoolReply,
)
from koyeb.api_async.models.list_service_pools_reply import (
    ListServicePoolsReply as AsyncListServicePoolsReply,
)
from koyeb.api_async.models.service_pool import ServicePool as AsyncServicePoolModel
from koyeb.api_async.models.service_pool_status import (
    ServicePoolStatus as AsyncServicePoolStatus,
)
from koyeb.api_async.models.update_service_pool_reply import (
    UpdateServicePoolReply as AsyncUpdateServicePoolReply,
)

from koyeb.sandbox.service_pool import AsyncServicePool, ServicePool, ServicePoolError
from koyeb.sandbox.utils import DEFAULT_HTTP_TIMEOUT

POOL_ID = "pool-1"
POOL_NAME = "my-pool"


def _pool_model(
    pool_id: str = POOL_ID,
    name: str = POOL_NAME,
    size: int = 3,
    ready_count: int = 3,
    status: ServicePoolStatus = ServicePoolStatus.READY,
) -> ServicePoolModel:
    return ServicePoolModel(
        id=pool_id, name=name, size=size, ready_count=ready_count, status=status
    )


def _async_pool_model(
    pool_id: str = POOL_ID,
    name: str = POOL_NAME,
    size: int = 3,
    ready_count: int = 3,
    status: AsyncServicePoolStatus = AsyncServicePoolStatus.READY,
) -> AsyncServicePoolModel:
    return AsyncServicePoolModel(
        id=pool_id, name=name, size=size, ready_count=ready_count, status=status
    )


def _create_reply() -> CreateServicePoolReply:
    return CreateServicePoolReply(service_pool=_pool_model())


def _get_reply() -> GetServicePoolReply:
    return GetServicePoolReply(service_pool=_pool_model())


def _list_reply() -> ListServicePoolsReply:
    return ListServicePoolsReply(
        service_pools=[_pool_model(), _pool_model(pool_id="pool-2")]
    )


def _update_reply(size: int = 5) -> UpdateServicePoolReply:
    return UpdateServicePoolReply(service_pool=_pool_model(size=size))


def _async_create_reply() -> AsyncCreateServicePoolReply:
    return AsyncCreateServicePoolReply(service_pool=_async_pool_model())


def _async_get_reply() -> AsyncGetServicePoolReply:
    return AsyncGetServicePoolReply(service_pool=_async_pool_model())


def _async_list_reply() -> AsyncListServicePoolsReply:
    return AsyncListServicePoolsReply(
        service_pools=[_async_pool_model(), _async_pool_model(pool_id="pool-2")]
    )


def _async_update_reply(size: int = 5) -> AsyncUpdateServicePoolReply:
    return AsyncUpdateServicePoolReply(service_pool=_async_pool_model(size=size))


def _sync_clients(create=None, get=None, list_=None, update=None, delete=None):
    clients = MagicMock()
    clients.service_pools = MagicMock()
    clients.service_pools.create_service_pool = create or MagicMock(
        return_value=_create_reply()
    )
    clients.service_pools.get_service_pool = get or MagicMock(return_value=_get_reply())
    clients.service_pools.list_service_pools = list_ or MagicMock(
        return_value=_list_reply()
    )
    clients.service_pools.update_service_pool = update or MagicMock(
        return_value=_update_reply()
    )
    clients.service_pools.delete_service_pool = delete or MagicMock(
        return_value=object()
    )
    return clients


def _async_clients(create=None, get=None, list_=None, update=None, delete=None):
    clients = MagicMock()
    clients.service_pools = MagicMock()
    clients.service_pools.create_service_pool = create or AsyncMock(
        return_value=_async_create_reply()
    )
    clients.service_pools.get_service_pool = get or AsyncMock(
        return_value=_async_get_reply()
    )
    clients.service_pools.list_service_pools = list_ or AsyncMock(
        return_value=_async_list_reply()
    )
    clients.service_pools.update_service_pool = update or AsyncMock(
        return_value=_async_update_reply()
    )
    clients.service_pools.delete_service_pool = delete or AsyncMock(
        return_value=object()
    )
    return clients


class TestServicePool(unittest.TestCase):
    def test_create_returns_bound_pool(self):
        create = MagicMock(return_value=_create_reply())
        clients = _sync_clients(create=create)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            pool = ServicePool.create(POOL_NAME, 3)
        create.assert_called_once()
        kwargs = create.call_args.kwargs
        self.assertEqual(kwargs["service_pool"].name, POOL_NAME)
        self.assertEqual(kwargs["service_pool"].size, 3)
        self.assertEqual(kwargs["_request_timeout"], DEFAULT_HTTP_TIMEOUT)
        self.assertEqual(pool.pool_id, POOL_ID)
        self.assertEqual(pool.name, POOL_NAME)
        self.assertEqual(pool.size, 3)
        self.assertEqual(pool.status, "READY")

    def test_create_accepts_definition_dict(self):
        create = MagicMock(return_value=_create_reply())
        clients = _sync_clients(create=create)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            ServicePool.create(POOL_NAME, 3, definition={"regions": ["na"]})
        body = create.call_args.kwargs["service_pool"]
        self.assertEqual(body.definition.regions, ["na"])

    def test_create_rejects_negative_size(self):
        with self.assertRaises(ValueError):
            ServicePool.create(POOL_NAME, -1)

    def test_create_accepts_size_zero(self):
        create = MagicMock(return_value=_create_reply())
        clients = _sync_clients(create=create)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            ServicePool.create(POOL_NAME, 0)
        self.assertEqual(create.call_args.kwargs["service_pool"].size, 0)

    def test_create_wraps_bad_definition_dict(self):
        create = MagicMock(return_value=_create_reply())
        clients = _sync_clients(create=create)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            with self.assertRaises(ServicePoolError) as ctx:
                ServicePool.create(POOL_NAME, 3, definition={"regions": "not-a-list"})
        self.assertIn("invalid deployment definition", str(ctx.exception))

    def test_create_requires_name_and_size(self):
        with self.assertRaises(ValueError):
            ServicePool.create("", 3)
        with self.assertRaises(ValueError):
            ServicePool.create(POOL_NAME, None)  # type: ignore[arg-type]

    def test_create_raises_pool_error_on_api_failure(self):
        clients = _sync_clients(
            create=MagicMock(side_effect=ApiException(status=400, reason="bad name"))
        )
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            with self.assertRaises(ServicePoolError) as ctx:
                ServicePool.create(POOL_NAME, 3)
        self.assertIn("bad name", str(ctx.exception))

    def test_get_returns_pool(self):
        get = MagicMock(return_value=_get_reply())
        clients = _sync_clients(get=get)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            pool = ServicePool.get(POOL_ID)
        get.assert_called_once_with(POOL_ID, _request_timeout=DEFAULT_HTTP_TIMEOUT)
        self.assertEqual(pool.pool_id, POOL_ID)

    def test_get_requires_pool_id(self):
        with self.assertRaises(ValueError):
            ServicePool.get("")

    def test_list_returns_all_pools(self):
        list_ = MagicMock(return_value=_list_reply())
        clients = _sync_clients(list_=list_)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            pools = ServicePool.list()
        self.assertEqual(len(pools), 2)
        self.assertEqual({p.pool_id for p in pools}, {POOL_ID, "pool-2"})

    def test_list_passes_name_filter(self):
        list_ = MagicMock(return_value=_list_reply())
        clients = _sync_clients(list_=list_)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            ServicePool.list(name="my-pool")
        self.assertEqual(list_.call_args.kwargs["name"], "my-pool")

    def test_list_passes_limit_offset_as_strings(self):
        list_ = MagicMock(return_value=_list_reply())
        clients = _sync_clients(list_=list_)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            ServicePool.list(limit=10, offset=5)
        kwargs = list_.call_args.kwargs
        # The generated API takes StrictStr under @validate_call; ints would
        # raise pydantic ValidationError before any HTTP call.
        self.assertEqual(kwargs["limit"], "10")
        self.assertEqual(kwargs["offset"], "5")

    def test_list_drops_entries_without_id(self):
        list_ = MagicMock(
            return_value=ListServicePoolsReply(
                service_pools=[_pool_model(), ServicePoolModel(name="orphan")]
            )
        )
        clients = _sync_clients(list_=list_)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            pools = ServicePool.list()
        self.assertEqual([p.pool_id for p in pools], [POOL_ID])

    def test_update_rejects_negative_size(self):
        pool = ServicePool(pool_id=POOL_ID)
        with self.assertRaises(ValueError):
            pool.update(definition={"regions": ["na"]}, size=-1)

    def test_update_requires_definition(self):
        pool = ServicePool(pool_id=POOL_ID)
        with self.assertRaises(ValueError):
            pool.update(definition=None)

    def test_update_sends_no_mask_and_full_body(self):
        update = MagicMock(return_value=_update_reply(size=5))
        clients = _sync_clients(update=update)
        pool = ServicePool(pool_id=POOL_ID, api_token=None, host=None)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            pool.update(definition={"regions": ["na"]}, size=5)
        args, kwargs = update.call_args
        self.assertEqual(args[0], POOL_ID)
        # The server rejects any non-empty update_mask — the wrapper never sends one.
        self.assertNotIn("update_mask", kwargs)
        self.assertEqual(kwargs["service_pool"].size, 5)
        self.assertEqual(kwargs["service_pool"].definition.regions, ["na"])
        # in place mutated
        self.assertEqual(pool.size, 5)

    def test_update_definition_only(self):
        update = MagicMock(return_value=_update_reply())
        clients = _sync_clients(update=update)
        pool = ServicePool(pool_id=POOL_ID)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            pool.update(definition={"regions": ["eu"]})
        self.assertIsNone(update.call_args.kwargs["service_pool"].size)
        self.assertEqual(
            update.call_args.kwargs["service_pool"].definition.regions, ["eu"]
        )

    def test_update_raises_on_api_failure(self):
        clients = _sync_clients(
            update=MagicMock(side_effect=ApiException(status=409, reason="conflict"))
        )
        pool = ServicePool(pool_id=POOL_ID)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            with self.assertRaises(ServicePoolError) as ctx:
                pool.update(definition={"regions": ["na"]})
        self.assertIn("conflict", str(ctx.exception))

    def test_delete_calls_endpoint(self):
        delete = MagicMock(return_value=object())
        clients = _sync_clients(delete=delete)
        pool = ServicePool(pool_id=POOL_ID)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            pool.delete()
        delete.assert_called_once_with(POOL_ID, _request_timeout=DEFAULT_HTTP_TIMEOUT)

    def test_delete_raises_on_api_failure(self):
        clients = _sync_clients(
            delete=MagicMock(side_effect=ApiException(status=404, reason="not found"))
        )
        pool = ServicePool(pool_id=POOL_ID)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            with self.assertRaises(ServicePoolError) as ctx:
                pool.delete()
        self.assertIn("not found", str(ctx.exception))

    def test_refresh_refetches_in_place(self):
        get = MagicMock(return_value=_get_reply())
        clients = _sync_clients(get=get)
        pool = ServicePool(pool_id=POOL_ID, name="old", size=1)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            pool.refresh()
        self.assertEqual(pool.name, POOL_NAME)
        self.assertEqual(pool.size, 3)

    def test_create_accepts_definition_model(self):
        create = MagicMock(return_value=_create_reply())
        clients = _sync_clients(create=create)
        definition = DeploymentDefinition(regions=["na"])
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            ServicePool.create(POOL_NAME, 3, definition=definition)
        # A ready-made model is passed through untouched, not rebuilt.
        self.assertIs(create.call_args.kwargs["service_pool"].definition, definition)

    def test_get_raises_on_api_failure(self):
        clients = _sync_clients(
            get=MagicMock(side_effect=ApiException(status=404, reason="no pool"))
        )
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            with self.assertRaises(ServicePoolError) as ctx:
                ServicePool.get(POOL_ID)
        self.assertIn("no pool", str(ctx.exception))

    def test_list_raises_on_api_failure(self):
        clients = _sync_clients(
            list_=MagicMock(side_effect=ApiException(status=403, reason="forbidden"))
        )
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            with self.assertRaises(ServicePoolError) as ctx:
                ServicePool.list()
        self.assertIn("forbidden", str(ctx.exception))

    def test_refresh_raises_on_api_failure(self):
        clients = _sync_clients(
            get=MagicMock(side_effect=ApiException(status=500, reason="boom"))
        )
        pool = ServicePool(pool_id=POOL_ID)
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            with self.assertRaises(ServicePoolError) as ctx:
                pool.refresh()
        self.assertIn("boom", str(ctx.exception))

    def test_error_detail_includes_response_body(self):
        clients = _sync_clients(
            create=MagicMock(
                side_effect=ApiException(
                    status=400,
                    reason="bad name",
                    body=b'{"message": "name already exists"}',
                )
            )
        )
        with patch("koyeb.sandbox.service_pool.get_api_clients", return_value=clients):
            with self.assertRaises(ServicePoolError) as ctx:
                ServicePool.create(POOL_NAME, 3)
        self.assertIn("bad name", str(ctx.exception))
        self.assertIn("name already exists", str(ctx.exception))

    def test_from_reply_raises_on_missing_service_pool(self):
        from koyeb.api.models.get_service_pool_reply import GetServicePoolReply

        reply = GetServicePoolReply(service_pool=None)
        with self.assertRaises(ServicePoolError):
            ServicePool._from_reply(reply, None, None)

    def test_repr_includes_identity(self):
        pool = ServicePool(pool_id=POOL_ID, name=POOL_NAME, size=3, status="READY")
        r = repr(pool)
        self.assertIn(f"pool_id={POOL_ID!r}", r)
        self.assertIn(f"name={POOL_NAME!r}", r)
        self.assertIn("status='READY'", r)


class TestAsyncServicePool(unittest.TestCase):
    def test_async_create(self):
        clients = _async_clients()
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            pool = asyncio.run(AsyncServicePool.create(POOL_NAME, 3))
        self.assertEqual(pool.pool_id, POOL_ID)
        clients.service_pools.create_service_pool.assert_awaited_once()

    def test_async_get(self):
        clients = _async_clients()
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            pool = asyncio.run(AsyncServicePool.get(POOL_ID))
        self.assertEqual(pool.pool_id, POOL_ID)
        clients.service_pools.get_service_pool.assert_awaited_once()

    def test_async_list_str_limit(self):
        clients = _async_clients()
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            pools = asyncio.run(AsyncServicePool.list(limit=10, offset=5))
        self.assertEqual(len(pools), 2)
        self.assertEqual(
            clients.service_pools.list_service_pools.call_args.kwargs["limit"], "10"
        )

    def test_async_update_sends_no_mask(self):
        clients = _async_clients()
        pool = AsyncServicePool(pool_id=POOL_ID)
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            asyncio.run(pool.update(definition={"regions": ["na"]}, size=5))
        kwargs = clients.service_pools.update_service_pool.call_args.kwargs
        self.assertNotIn("update_mask", kwargs)
        self.assertEqual(kwargs["service_pool"].size, 5)

    def test_async_update_requires_definition(self):
        pool = AsyncServicePool(pool_id=POOL_ID)
        with self.assertRaises(ValueError):
            asyncio.run(pool.update(definition=None))

    def test_async_delete(self):
        clients = _async_clients()
        pool = AsyncServicePool(pool_id=POOL_ID)
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            asyncio.run(pool.delete())
        clients.service_pools.delete_service_pool.assert_awaited_once()

    def test_async_delete_raises_on_api_failure(self):
        clients = _async_clients(
            delete=AsyncMock(
                side_effect=AsyncApiException(status=404, reason="missing")
            )
        )
        pool = AsyncServicePool(pool_id=POOL_ID)
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            with self.assertRaises(ServicePoolError) as ctx:
                asyncio.run(pool.delete())
        self.assertIn("missing", str(ctx.exception))

    def test_async_refresh(self):
        clients = _async_clients()
        pool = AsyncServicePool(pool_id=POOL_ID, name="old")
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            asyncio.run(pool.refresh())
        self.assertEqual(pool.name, POOL_NAME)

    def test_async_update_raises_on_api_failure(self):
        clients = _async_clients(
            update=AsyncMock(side_effect=AsyncApiException(status=409, reason="bad"))
        )
        pool = AsyncServicePool(pool_id=POOL_ID)
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            with self.assertRaises(ServicePoolError) as ctx:
                asyncio.run(pool.update(definition={"regions": ["na"]}))
        self.assertIn("bad", str(ctx.exception))

    def test_async_refresh_raises_on_api_failure(self):
        clients = _async_clients(
            get=AsyncMock(side_effect=AsyncApiException(status=404, reason="gone"))
        )
        pool = AsyncServicePool(pool_id=POOL_ID)
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            with self.assertRaises(ServicePoolError) as ctx:
                asyncio.run(pool.refresh())
        self.assertIn("gone", str(ctx.exception))

    def test_async_create_raises_on_api_failure(self):
        clients = _async_clients(
            create=AsyncMock(side_effect=AsyncApiException(status=400, reason="bad"))
        )
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            with self.assertRaises(ServicePoolError):
                asyncio.run(AsyncServicePool.create(POOL_NAME, 3))

    def test_async_create_requires_name_and_size(self):
        with self.assertRaises(ValueError):
            asyncio.run(AsyncServicePool.create("", 3))
        with self.assertRaises(ValueError):
            asyncio.run(AsyncServicePool.create(POOL_NAME, None))  # type: ignore[arg-type]

    def test_async_create_rejects_negative_size(self):
        with self.assertRaises(ValueError):
            asyncio.run(AsyncServicePool.create(POOL_NAME, -1))

    def test_async_get_requires_pool_id(self):
        with self.assertRaises(ValueError):
            asyncio.run(AsyncServicePool.get(""))

    def test_async_get_raises_on_api_failure(self):
        clients = _async_clients(
            get=AsyncMock(side_effect=AsyncApiException(status=404, reason="gone"))
        )
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            with self.assertRaises(ServicePoolError) as ctx:
                asyncio.run(AsyncServicePool.get(POOL_ID))
        self.assertIn("gone", str(ctx.exception))

    def test_async_list_passes_name_filter(self):
        clients = _async_clients()
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            asyncio.run(AsyncServicePool.list(name=POOL_NAME))
        self.assertEqual(
            clients.service_pools.list_service_pools.call_args.kwargs["name"],
            POOL_NAME,
        )

    def test_async_list_raises_on_api_failure(self):
        clients = _async_clients(
            list_=AsyncMock(side_effect=AsyncApiException(status=403, reason="denied"))
        )
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            with self.assertRaises(ServicePoolError) as ctx:
                asyncio.run(AsyncServicePool.list())
        self.assertIn("denied", str(ctx.exception))

    def test_async_list_drops_entries_without_id(self):
        clients = _async_clients(
            list_=AsyncMock(
                return_value=AsyncListServicePoolsReply(
                    service_pools=[
                        _async_pool_model(),
                        AsyncServicePoolModel(name="orphan"),
                    ]
                )
            )
        )
        with patch(
            "koyeb.sandbox.service_pool.get_async_api_clients", return_value=clients
        ):
            pools = asyncio.run(AsyncServicePool.list())
        self.assertEqual([p.pool_id for p in pools], [POOL_ID])

    def test_async_update_rejects_negative_size(self):
        pool = AsyncServicePool(pool_id=POOL_ID)
        with self.assertRaises(ValueError):
            asyncio.run(pool.update(definition={"regions": ["na"]}, size=-1))


if __name__ == "__main__":
    unittest.main()
