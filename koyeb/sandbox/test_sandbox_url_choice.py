"""exec/files use the in-cluster URL when reachable; URLs handed to users
(get_domain) always stay public."""

import unittest
from types import SimpleNamespace
from unittest import mock

from koyeb.sandbox.sandbox import Sandbox

PUBLIC = "https://sandboxes.example.com"
INTERNAL = "http://sandbox-gateway.koyeb.svc.cluster.local"


def _clients():
    deployment = SimpleNamespace(
        metadata=SimpleNamespace(
            sandbox=SimpleNamespace(
                public_url=PUBLIC, internal_url=INTERNAL, routing_key="rk"
            )
        )
    )
    return SimpleNamespace(
        deployments=SimpleNamespace(
            get_deployment=lambda id: SimpleNamespace(deployment=deployment)
        )
    )


class TestSandboxUrlChoice(unittest.TestCase):
    def setUp(self):
        self.sandbox = Sandbox(sandbox_id="svc-1", app_id="app-1", service_id="svc-1")
        self.sandbox._deployment_id = "depl-1"
        patches = [
            mock.patch(
                "koyeb.sandbox.clients.get_api_clients", return_value=_clients()
            ),
            mock.patch("koyeb.sandbox.control_plane._resolves", return_value=True),
            mock.patch.dict("os.environ", {"KOYEB_SANDBOX_URL": ""}),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def test_exec_uses_internal_url_in_cluster(self):
        self.assertEqual(
            self.sandbox._get_sandbox_url(), (f"{INTERNAL}/koyeb-sandbox", "rk")
        )

    def test_get_domain_stays_public_in_cluster(self):
        self.assertEqual(self.sandbox.get_domain(), "sandboxes.example.com/r/rk/")


if __name__ == "__main__":
    unittest.main()
