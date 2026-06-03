import unittest
from unittest.mock import patch

from koyeb.api.models.deployment_definition_type import DeploymentDefinitionType
from koyeb.api.models.deployment_mesh import DeploymentMesh
from koyeb.api.models.docker_source import DockerSource
from koyeb.sandbox.utils import (
    build_env_vars,
    create_deployment_definition,
    create_docker_source,
)


class TestCreateDockerSource(unittest.TestCase):
    """Tests for create_docker_source entrypoint, command, and args support."""

    def test_default_no_entrypoint_no_command(self):
        ds = create_docker_source("myimage")
        self.assertIsNone(ds.command)
        self.assertIsNone(ds.args)
        self.assertIsNone(ds.entrypoint)

    def test_command_and_args(self):
        ds = create_docker_source("myimage", command="python", args=["-u", "app.py"])
        self.assertEqual(ds.command, "python")
        self.assertEqual(ds.args, ["-u", "app.py"])
        self.assertIsNone(ds.entrypoint)

    def test_command_only(self):
        ds = create_docker_source("myimage", command="python app.py")
        self.assertEqual(ds.command, "python app.py")
        self.assertIsNone(ds.args)
        self.assertIsNone(ds.entrypoint)

    def test_entrypoint_only(self):
        ds = create_docker_source("myimage", entrypoint=["/bin/sh", "-c"])
        self.assertIsNone(ds.command)
        self.assertIsNone(ds.args)
        self.assertEqual(ds.entrypoint, ["/bin/sh", "-c"])

    def test_entrypoint_and_command(self):
        ds = create_docker_source(
            "myimage", entrypoint=["/bin/sh", "-c"], command="python app.py"
        )
        self.assertEqual(ds.command, "python app.py")
        self.assertEqual(ds.entrypoint, ["/bin/sh", "-c"])
        self.assertIsNone(ds.args)

    def test_entrypoint_command_and_args(self):
        ds = create_docker_source(
            "myimage", entrypoint=["/bin/sh", "-c"], command="python", args=["app.py"]
        )
        self.assertEqual(ds.command, "python")
        self.assertEqual(ds.entrypoint, ["/bin/sh", "-c"])
        self.assertEqual(ds.args, ["app.py"])

    def test_privileged_and_registry_secret_still_work(self):
        ds = create_docker_source(
            "myimage",
            privileged=True,
            image_registry_secret="my-secret",
            entrypoint=["/entrypoint.sh"],
            command="serve",
        )
        self.assertTrue(ds.privileged)
        self.assertEqual(ds.image_registry_secret, "my-secret")
        self.assertEqual(ds.entrypoint, ["/entrypoint.sh"])
        self.assertEqual(ds.command, "serve")


class TestCreateDeploymentDefinition(unittest.TestCase):
    """Tests for sandbox deployment definition mesh configuration."""

    def _create_definition(self, enable_mesh=None):
        return create_deployment_definition(
            name="sandbox",
            docker_source=DockerSource(image="myimage"),
            env_vars=build_env_vars({}),
            instance_type="micro",
            enable_mesh=enable_mesh,
        )

    def test_mesh_auto_by_default(self):
        definition = self._create_definition()
        self.assertEqual(definition.type, DeploymentDefinitionType.SANDBOX)
        self.assertEqual(definition.mesh, DeploymentMesh.DEPLOYMENT_MESH_AUTO)

    def test_mesh_enabled_when_requested(self):
        definition = self._create_definition(enable_mesh=True)
        self.assertEqual(definition.mesh, DeploymentMesh.DEPLOYMENT_MESH_ENABLED)

    def test_mesh_disabled_when_requested(self):
        definition = self._create_definition(enable_mesh=False)
        self.assertEqual(definition.mesh, DeploymentMesh.DEPLOYMENT_MESH_DISABLED)

    @patch.dict("os.environ", {"KOYEB_K8S_REGION": "par"})
    def test_koyeb_k8s_region_disables_mesh(self):
        definition = self._create_definition(enable_mesh=True)
        self.assertEqual(definition.mesh, DeploymentMesh.DEPLOYMENT_MESH_DISABLED)

    @patch.dict("os.environ", {"KOYEB_K8S_REGION": ""})
    def test_empty_koyeb_k8s_region_disables_mesh(self):
        definition = self._create_definition(enable_mesh=True)
        self.assertEqual(definition.mesh, DeploymentMesh.DEPLOYMENT_MESH_DISABLED)


if __name__ == "__main__":
    unittest.main()
