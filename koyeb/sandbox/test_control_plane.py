"""Pins the control-plane seam: neutral info types out, payloads in,
error mapping exactly where the orchestration contract demands it."""

import asyncio
import os
import socket
import unittest
from unittest import mock
from types import SimpleNamespace

from koyeb.api.exceptions import ApiException, NotFoundException
from koyeb.api_async.exceptions import (
    NotFoundException as AsyncNotFoundException,
)

from koyeb.sandbox.control_plane import (
    AsyncControlPlane,
    DeploymentInfo,
    ServiceInfo,
    SyncControlPlane,
    select_sandbox_url,
    select_sandbox_url_async,
)
from koyeb.sandbox.errors import SandboxError


def _fake_service():
    return SimpleNamespace(
        id="svc-1",
        app_id="app-1",
        name="sb-1",
        active_deployment_id="depl-active",
        latest_deployment_id="depl-latest",
    )


def _fake_deployment():
    return SimpleNamespace(
        id="depl-active",
        status="HEALTHY",
        definition=SimpleNamespace(
            env=[SimpleNamespace(key="SANDBOX_SECRET", value="sec")],
            to_dict=lambda: {"env": [{"key": "SANDBOX_SECRET", "value": "sec"}]},
        ),
        metadata=SimpleNamespace(
            sandbox=SimpleNamespace(public_url="https://sb.example", routing_key="rk"),
            proxy_ports=[SimpleNamespace(port=3031, host="h", public_port=1)],
        ),
    )


class TestSyncControlPlane(unittest.TestCase):
    def _clients(self, **overrides):
        defaults = dict(
            apps=SimpleNamespace(
                get_app=lambda app_id: SimpleNamespace(
                    app=SimpleNamespace(
                        id=app_id,
                        name="sb-app",
                        domains=[SimpleNamespace(name="d.example")],
                    )
                )
            ),
            services=SimpleNamespace(
                get_service=lambda id: SimpleNamespace(service=_fake_service()),
                update_service=lambda id, service: SimpleNamespace(
                    service=SimpleNamespace(latest_deployment_id="depl-new")
                ),
            ),
            deployments=SimpleNamespace(
                get_deployment=lambda id: SimpleNamespace(deployment=_fake_deployment())
            ),
        )
        defaults.update(overrides)
        return SimpleNamespace(**defaults)

    def test_get_service_maps_to_neutral_info(self):
        cp = SyncControlPlane(self._clients())
        service = cp.get_service("svc-1")
        self.assertEqual(
            service,
            ServiceInfo(
                id="svc-1",
                app_id="app-1",
                name="sb-1",
                active_deployment_id="depl-active",
                latest_deployment_id="depl-latest",
            ),
        )

    def test_get_service_not_found_maps_to_sandbox_error(self):
        def raise_not_found(id):
            raise NotFoundException(status=404, reason="Not Found")

        cp = SyncControlPlane(
            self._clients(services=SimpleNamespace(get_service=raise_not_found))
        )
        with self.assertRaises(SandboxError) as cm:
            cp.get_service("svc-1")
        self.assertIn("Sandbox not found with id: svc-1", str(cm.exception))

    def test_get_service_api_error_maps_to_sandbox_error(self):
        def raise_api(id):
            raise ApiException(status=500, reason="Internal Server Error")

        cp = SyncControlPlane(
            self._clients(services=SimpleNamespace(get_service=raise_api))
        )
        with self.assertRaises(SandboxError) as cm:
            cp.get_service("svc-1")
        self.assertIn("Failed to retrieve sandbox with id: svc-1", str(cm.exception))

    def test_get_service_none_service_maps_not_found(self):
        cp = SyncControlPlane(
            self._clients(
                services=SimpleNamespace(
                    get_service=lambda id: SimpleNamespace(service=None)
                )
            )
        )
        with self.assertRaises(SandboxError) as cm:
            cp.get_service("svc-1")
        self.assertIn("Sandbox not found with id: svc-1", str(cm.exception))

    def test_get_deployment_extracts_env_metadata_proxy_ports(self):
        cp = SyncControlPlane(self._clients())
        deployment = cp.get_deployment("depl-active")
        self.assertIsInstance(deployment, DeploymentInfo)
        self.assertEqual(deployment.env, {"SANDBOX_SECRET": "sec"})
        self.assertEqual(deployment.sandbox_url, "https://sb.example")
        self.assertEqual(deployment.routing_key, "rk")
        self.assertEqual(
            deployment.proxy_ports, [{"port": 3031, "host": "h", "public_port": 1}]
        )
        self.assertEqual(deployment.status, "HEALTHY")

    def test_get_app_returns_domain_names(self):
        cp = SyncControlPlane(self._clients())
        app = cp.get_app("app-1")
        self.assertEqual(app.id, "app-1")
        self.assertEqual(app.domains, ["d.example"])

    def test_list_services_filters_sandbox_type_with_string_pagination(self):
        calls = []

        def list_services(**kwargs):
            calls.append(kwargs)
            return SimpleNamespace(services=[_fake_service()], count=1, has_next=False)

        cp = SyncControlPlane(
            self._clients(services=SimpleNamespace(list_services=list_services))
        )
        services, count = cp.list_services(
            app_id="app-1", name="sb", offset=0, limit=100
        )
        self.assertEqual(count, 1)
        self.assertEqual(services[0].id, "svc-1")
        self.assertEqual(calls[0]["types"], ["SANDBOX"])
        self.assertEqual(calls[0]["app_id"], "app-1")
        self.assertEqual(calls[0]["name"], "sb")
        self.assertEqual(calls[0]["limit"], "100")
        self.assertEqual(calls[0]["offset"], "0")

    def test_update_service_coerces_definition_dict(self):
        sent = []

        def update_service(id, service):
            sent.append(service)
            return SimpleNamespace(
                service=SimpleNamespace(latest_deployment_id="depl-new")
            )

        cp = SyncControlPlane(
            self._clients(services=SimpleNamespace(update_service=update_service))
        )
        new_id = cp.update_service("svc-1", {"env": []})
        self.assertEqual(new_id, "depl-new")
        self.assertIsNotNone(sent[0].definition)

    def test_deployment_definition_returns_wire_dict(self):
        cp = SyncControlPlane(self._clients())
        self.assertEqual(
            cp.deployment_definition("depl-active"),
            {"env": [{"key": "SANDBOX_SECRET", "value": "sec"}]},
        )

    def test_create_app_and_service_return_ids(self):
        cp = SyncControlPlane(
            self._clients(
                apps=SimpleNamespace(
                    create_app=lambda app: SimpleNamespace(
                        app=SimpleNamespace(id="app-1")
                    )
                ),
                services=SimpleNamespace(
                    create_service=lambda service: SimpleNamespace(
                        service=SimpleNamespace(id="svc-1")
                    )
                ),
            )
        )
        self.assertEqual(cp.create_app({"name": "a", "life_cycle": {}}), "app-1")
        self.assertEqual(cp.create_service({"app_id": "app-1"}), "svc-1")


class TestAsyncControlPlane(unittest.TestCase):
    def _clients(self, **overrides):
        async def get_service(id):
            return SimpleNamespace(service=_fake_service())

        async def get_deployment(id):
            return SimpleNamespace(deployment=_fake_deployment())

        async def get_app(app_id):
            return SimpleNamespace(
                app=SimpleNamespace(
                    id=app_id,
                    name="sb-app",
                    domains=[SimpleNamespace(name="d.example")],
                )
            )

        defaults = dict(
            apps=SimpleNamespace(get_app=get_app),
            services=SimpleNamespace(get_service=get_service),
            deployments=SimpleNamespace(get_deployment=get_deployment),
        )
        defaults.update(overrides)
        return SimpleNamespace(**defaults)

    def test_get_service_maps_to_neutral_info(self):
        cp = AsyncControlPlane(self._clients())
        service = asyncio.run(cp.get_service("svc-1"))
        self.assertEqual(service.id, "svc-1")
        self.assertEqual(service.active_deployment_id, "depl-active")

    def test_get_service_not_found_maps_to_sandbox_error(self):
        async def raise_not_found(id):
            raise AsyncNotFoundException(status=404, reason="Not Found")

        cp = AsyncControlPlane(
            self._clients(services=SimpleNamespace(get_service=raise_not_found))
        )
        with self.assertRaises(SandboxError) as cm:
            asyncio.run(cp.get_service("svc-1"))
        self.assertIn("Sandbox not found with id: svc-1", str(cm.exception))

    def test_get_deployment_extracts_env_metadata_proxy_ports(self):
        cp = AsyncControlPlane(self._clients())
        deployment = asyncio.run(cp.get_deployment("depl-active"))
        self.assertEqual(deployment.env, {"SANDBOX_SECRET": "sec"})
        self.assertEqual(deployment.sandbox_url, "https://sb.example")
        self.assertEqual(
            deployment.proxy_ports, [{"port": 3031, "host": "h", "public_port": 1}]
        )

    def test_list_services_filters_sandbox_type_with_string_pagination(self):
        calls = []

        async def list_services(**kwargs):
            calls.append(kwargs)
            return SimpleNamespace(services=[_fake_service()], count=1, has_next=False)

        cp = AsyncControlPlane(
            self._clients(services=SimpleNamespace(list_services=list_services))
        )
        services, count = asyncio.run(
            cp.list_services(app_id="app-1", name="sb", offset=0, limit=100)
        )
        self.assertEqual(count, 1)
        self.assertEqual(calls[0]["types"], ["SANDBOX"])
        self.assertEqual(calls[0]["limit"], "100")

    def test_deployment_definition_returns_wire_dict(self):
        cp = AsyncControlPlane(self._clients())
        self.assertEqual(
            asyncio.run(cp.deployment_definition("depl-active")),
            {"env": [{"key": "SANDBOX_SECRET", "value": "sec"}]},
        )

    def test_update_service_coerces_definition_dict(self):
        sent = []

        async def update_service(id, service):
            sent.append(service)
            return SimpleNamespace(
                service=SimpleNamespace(latest_deployment_id="depl-new")
            )

        cp = AsyncControlPlane(
            self._clients(services=SimpleNamespace(update_service=update_service))
        )
        new_id = asyncio.run(cp.update_service("svc-1", {"env": []}))
        self.assertEqual(new_id, "depl-new")
        self.assertIsNotNone(sent[0].definition)


class TestSelectSandboxUrl(unittest.TestCase):
    PUBLIC = "https://sandboxes.example.com"
    INTERNAL = "http://sandbox-gateway.koyeb.svc.cluster.local"

    def _meta(self, internal=INTERNAL):
        return SimpleNamespace(public_url=self.PUBLIC, internal_url=internal)

    def _select(self, meta, resolves, extra_env=None, in_pod=True):
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in ("KOYEB_SANDBOX_URL", "KUBERNETES_SERVICE_HOST")
        }
        if in_pod:
            env["KUBERNETES_SERVICE_HOST"] = "10.0.0.1"
        env.update(extra_env or {})
        with mock.patch.dict(os.environ, env, clear=True), mock.patch(
            "koyeb.sandbox.control_plane._resolves", return_value=resolves
        ):
            return select_sandbox_url(meta)

    def test_no_internal_url_uses_public(self):
        self.assertEqual(self._select(self._meta(internal=None), True), self.PUBLIC)

    def test_old_model_without_field_uses_public(self):
        meta = SimpleNamespace(public_url=self.PUBLIC)
        self.assertEqual(self._select(meta, True), self.PUBLIC)

    def test_in_cluster_uses_internal(self):
        self.assertEqual(self._select(self._meta(), True), self.INTERNAL)

    def test_outside_cluster_uses_public(self):
        self.assertEqual(self._select(self._meta(), False), self.PUBLIC)

    def test_env_forces_public(self):
        env = {"KOYEB_SANDBOX_URL": "public"}
        self.assertEqual(self._select(self._meta(), True, env), self.PUBLIC)

    def test_env_forces_internal(self):
        env = {"KOYEB_SANDBOX_URL": "internal"}
        self.assertEqual(self._select(self._meta(), False, env), self.INTERNAL)

    def test_outside_kubernetes_skips_lookup(self):
        with mock.patch("koyeb.sandbox.control_plane.socket.getaddrinfo") as lookup:
            url = self._select_real_dns(self._meta(), in_pod=False)
        self.assertEqual(url, self.PUBLIC)
        lookup.assert_not_called()

    def test_env_url_override(self):
        env = {"KOYEB_SANDBOX_URL": "https://gw.custom.example/"}
        self.assertEqual(
            self._select(self._meta(), True, env), "https://gw.custom.example"
        )

    def test_env_url_override_without_internal_url(self):
        env = {"KOYEB_SANDBOX_URL": "https://gw.custom.example"}
        self.assertEqual(
            self._select(self._meta(internal=None), False, env, in_pod=False),
            "https://gw.custom.example",
        )

    def test_failed_lookup_is_not_cached(self):
        host = "sandbox-gateway.retry-test.svc"
        meta = self._meta(internal=f"http://{host}")
        calls = [socket.gaierror(), [("ok",)]]

        def fake_lookup(*args, **kwargs):
            result = calls.pop(0)
            if isinstance(result, Exception):
                raise result
            return result

        with mock.patch(
            "koyeb.sandbox.control_plane.socket.getaddrinfo", side_effect=fake_lookup
        ):
            self.assertEqual(self._select_real_dns(meta), self.PUBLIC)
            self.assertEqual(self._select_real_dns(meta), meta.internal_url)

    def test_async_lookup_does_not_block(self):
        host = "sandbox-gateway.async-test.svc"
        meta = self._meta(internal=f"http://{host}")

        async def run():
            loop = asyncio.get_running_loop()
            with mock.patch.object(
                loop, "getaddrinfo", mock.AsyncMock(return_value=[("ok",)])
            ) as lookup, mock.patch(
                "koyeb.sandbox.control_plane.socket.getaddrinfo"
            ) as blocking:
                url = await select_sandbox_url_async(meta)
            lookup.assert_awaited_once()
            blocking.assert_not_called()
            return url

        with mock.patch.dict(
            os.environ, {"KUBERNETES_SERVICE_HOST": "10.0.0.1", "KOYEB_SANDBOX_URL": ""}
        ):
            self.assertEqual(asyncio.run(run()), meta.internal_url)

    def _select_real_dns(self, meta, in_pod=True):
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in ("KOYEB_SANDBOX_URL", "KUBERNETES_SERVICE_HOST")
        }
        if in_pod:
            env["KUBERNETES_SERVICE_HOST"] = "10.0.0.1"
        with mock.patch.dict(os.environ, env, clear=True):
            return select_sandbox_url(meta)

    def test_get_deployment_uses_selected_url(self):
        deployment = _fake_deployment()
        deployment.metadata.sandbox.internal_url = self.INTERNAL
        clients = SimpleNamespace(
            deployments=SimpleNamespace(
                get_deployment=lambda id: SimpleNamespace(deployment=deployment)
            )
        )
        with mock.patch(
            "koyeb.sandbox.control_plane._resolves", return_value=True
        ), mock.patch.dict(
            os.environ, {"KUBERNETES_SERVICE_HOST": "10.0.0.1", "KOYEB_SANDBOX_URL": ""}
        ):
            info = SyncControlPlane(clients).get_deployment("depl-1")
        self.assertEqual(info.sandbox_url, self.INTERNAL)


if __name__ == "__main__":
    unittest.main()
