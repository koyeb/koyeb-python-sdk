import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from koyeb.api.models.deployment_definition import DeploymentDefinition
from koyeb.api.models.egress_policy_mode import EgressPolicyMode
from koyeb.api_async.models.deployment_definition import (
    DeploymentDefinition as AsyncDeploymentDefinition,
)
from koyeb.sandbox.sandbox import AsyncSandbox, Sandbox
from koyeb.sandbox.utils import EgressPolicyError


class TestCreateEgressWiring(unittest.TestCase):
    """Tests that Sandbox.create wires egress kwargs into the deployment definition."""

    def _create(self, mock_get_clients, **kwargs):
        clients = MagicMock()
        clients.apps.create_app.return_value.app.id = "mock-app-id"
        mock_get_clients.return_value = clients
        Sandbox.create(name="t", api_token="tok", wait_ready=False, **kwargs)
        return clients.services.create_service.call_args.kwargs["service"]

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_default_sends_no_network_policy(self, mock_get_clients):
        service = self._create(mock_get_clients)
        self.assertIsNone(service.definition.network_policy)

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_block_network_sends_deny_all(self, mock_get_clients):
        service = self._create(mock_get_clients, block_network=True)
        egress = service.definition.network_policy.egress
        self.assertEqual(egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL)
        self.assertIsNone(egress.allow_list)

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_allowlist_sends_deny_all_with_destinations(self, mock_get_clients):
        service = self._create(
            mock_get_clients, outbound_allowlist=["1.2.3.4", "10.0.0.0/8"]
        )
        egress = service.definition.network_policy.egress
        self.assertEqual(egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL)
        self.assertEqual(
            [d.cidr for d in egress.allow_list], ["1.2.3.4/32", "10.0.0.0/8"]
        )

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_mutually_exclusive_fails_before_any_api_call(self, mock_get_clients):
        with self.assertRaises(EgressPolicyError):
            Sandbox.create(
                name="t",
                api_token="tok",
                wait_ready=False,
                block_network=True,
                outbound_allowlist=["1.2.3.4"],
            )
        mock_get_clients.assert_not_called()

    @patch("koyeb.sandbox.utils.get_async_api_clients")
    def test_async_create_forwards_egress_kwargs(self, mock_get_clients):
        clients = MagicMock()
        clients.apps.create_app = AsyncMock()
        clients.apps.create_app.return_value.app.id = "mock-app-id"
        clients.services.create_service = AsyncMock()
        mock_get_clients.return_value = clients
        asyncio.run(
            AsyncSandbox.create(
                name="t", api_token="tok", wait_ready=False, block_network=True
            )
        )
        service = clients.services.create_service.call_args.kwargs["service"]
        egress = service.definition.network_policy.egress
        self.assertEqual(egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL)

    @patch("koyeb.sandbox.utils.get_async_api_clients")
    def test_async_mutually_exclusive_fails_before_any_api_call(self, mock_get_clients):
        with self.assertRaises(EgressPolicyError):
            asyncio.run(
                AsyncSandbox.create(
                    name="t",
                    api_token="tok",
                    wait_ready=False,
                    block_network=True,
                    outbound_allowlist=["1.2.3.4"],
                )
            )
        mock_get_clients.assert_not_called()


def _make_clients():
    clients = MagicMock()
    clients.deployments.get_deployment.return_value.deployment.definition = (
        DeploymentDefinition(name="sb")
    )
    return clients


def _make_sandbox(cls=Sandbox):
    return cls(
        sandbox_id="sb",
        app_id="app-id",
        service_id="svc-id",
        name="sb",
        api_token="tok",
        sandbox_secret="secret",
    )


class TestUpdateNetworkPolicy(unittest.TestCase):
    """Tests for Sandbox.update_network_policy."""

    def _update(self, mock_get_clients, **kwargs):
        clients = _make_clients()
        mock_get_clients.return_value = clients
        _make_sandbox().update_network_policy(**kwargs)
        call = clients.services.update_service.call_args
        self.assertEqual(call.kwargs["id"], "svc-id")
        return call.kwargs["service"]

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_block_network(self, mock_get_clients):
        update = self._update(mock_get_clients, block_network=True)
        egress = update.definition.network_policy.egress
        self.assertEqual(egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL)
        self.assertIsNone(egress.allow_list)

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_allowlist(self, mock_get_clients):
        update = self._update(mock_get_clients, outbound_allowlist=["2001:db8::1"])
        egress = update.definition.network_policy.egress
        self.assertEqual(egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL)
        self.assertEqual([d.cidr for d in egress.allow_list], ["2001:db8::1/128"])

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_no_args_resets_to_default(self, mock_get_clients):
        update = self._update(mock_get_clients)
        egress = update.definition.network_policy.egress
        self.assertEqual(egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DEFAULT)
        self.assertIsNone(egress.allow_list)

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_mutually_exclusive_fails_before_any_api_call(self, mock_get_clients):
        with self.assertRaises(EgressPolicyError):
            _make_sandbox().update_network_policy(
                block_network=True, outbound_allowlist=["1.2.3.4"]
            )
        mock_get_clients.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_api_failure_wrapped_in_sandbox_error(self, mock_get_clients):
        from koyeb.sandbox.utils import SandboxError

        clients = _make_clients()
        clients.services.update_service.side_effect = RuntimeError("boom")
        mock_get_clients.return_value = clients
        with self.assertRaises(SandboxError):
            _make_sandbox().update_network_policy(block_network=True)

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_pins_new_deployment_and_resets_cached_state(self, mock_get_clients):
        clients = _make_clients()
        clients.services.update_service.return_value.service.latest_deployment_id = (
            "new-dep"
        )
        mock_get_clients.return_value = clients

        sandbox = _make_sandbox()
        stale_client = MagicMock()
        sandbox._deployment_id = "old-dep"
        sandbox._sandbox_url = ("https://old/koyeb-sandbox", "old-key")
        sandbox._url = "https://old"
        sandbox._domain = "old"
        sandbox._client = stale_client

        sandbox.update_network_policy(block_network=True)

        self.assertEqual(sandbox._deployment_id, "new-dep")
        self.assertIsNone(sandbox._sandbox_url)
        self.assertIsNone(sandbox._url)
        self.assertIsNone(sandbox._domain)
        self.assertIsNone(sandbox._client)
        stale_client.close.assert_called_once()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_falls_back_to_get_service_when_reply_lacks_deployment_id(
        self, mock_get_clients
    ):
        clients = _make_clients()
        clients.services.update_service.return_value.service.latest_deployment_id = None
        clients.services.get_service.return_value.service.latest_deployment_id = (
            "refetched-dep"
        )
        mock_get_clients.return_value = clients

        sandbox = _make_sandbox()
        sandbox.update_network_policy(block_network=True)

        self.assertEqual(sandbox._deployment_id, "refetched-dep")

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_resets_state_even_when_new_deployment_id_lookup_fails(
        self, mock_get_clients
    ):
        clients = _make_clients()
        clients.services.update_service.return_value.service.latest_deployment_id = None
        # First get_service call is the initial fetch; the fallback lookup after
        # the successful update fails.
        clients.services.get_service.side_effect = [
            clients.services.get_service.return_value,
            RuntimeError("api down"),
        ]
        mock_get_clients.return_value = clients

        sandbox = _make_sandbox()
        sandbox._deployment_id = "old-dep"
        sandbox._sandbox_url = ("https://old/koyeb-sandbox", "old-key")

        sandbox.update_network_policy(block_network=True)

        self.assertIsNone(sandbox._deployment_id)
        self.assertIsNone(sandbox._sandbox_url)


def _make_async_clients():
    clients = MagicMock()
    clients.services.get_service = AsyncMock()
    clients.services.get_service.return_value.service.latest_deployment_id = "dep-id"
    clients.deployments.get_deployment = AsyncMock()
    clients.deployments.get_deployment.return_value.deployment.definition = (
        AsyncDeploymentDefinition(name="sb")
    )
    clients.services.update_service = AsyncMock()
    return clients


class TestAsyncUpdateNetworkPolicy(unittest.TestCase):
    """Tests for AsyncSandbox.update_network_policy."""

    @patch("koyeb.sandbox.utils.get_async_api_clients")
    def test_async_block_network(self, mock_get_clients):
        clients = _make_async_clients()
        mock_get_clients.return_value = clients
        sandbox = _make_sandbox(AsyncSandbox)
        asyncio.run(sandbox.update_network_policy(block_network=True))
        update = clients.services.update_service.call_args.kwargs["service"]
        self.assertEqual(
            update.definition.network_policy.egress.mode,
            EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL,
        )

    @patch("koyeb.sandbox.utils.get_async_api_clients")
    def test_async_pins_new_deployment_and_resets_cached_state(self, mock_get_clients):
        clients = _make_async_clients()
        clients.services.update_service.return_value.service.latest_deployment_id = (
            "new-dep"
        )
        mock_get_clients.return_value = clients

        sandbox = _make_sandbox(AsyncSandbox)
        stale_async_client = AsyncMock()
        sandbox._deployment_id = "old-dep"
        sandbox._sandbox_url = ("https://old/koyeb-sandbox", "old-key")
        sandbox._url = "https://old"
        sandbox._async_client = stale_async_client

        asyncio.run(sandbox.update_network_policy(block_network=True))

        self.assertEqual(sandbox._deployment_id, "new-dep")
        self.assertIsNone(sandbox._sandbox_url)
        self.assertIsNone(sandbox._url)
        self.assertIsNone(sandbox._async_client)
        stale_async_client.close.assert_awaited_once()
