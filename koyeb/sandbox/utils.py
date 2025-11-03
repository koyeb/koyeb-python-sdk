# coding: utf-8

"""
Utility functions for Koyeb Sandbox
"""

import os
from typing import Dict, List, Optional

from koyeb.api import ApiClient, Configuration
from koyeb.api.api import AppsApi, InstancesApi, ServicesApi
from koyeb.api.exceptions import ApiException, NotFoundException
from koyeb.api.models.deployment_definition import DeploymentDefinition
from koyeb.api.models.deployment_definition_type import DeploymentDefinitionType
from koyeb.api.models.deployment_env import DeploymentEnv
from koyeb.api.models.deployment_instance_type import DeploymentInstanceType
from koyeb.api.models.deployment_port import DeploymentPort
from koyeb.api.models.deployment_scaling import DeploymentScaling
from koyeb.api.models.docker_source import DockerSource
from koyeb.api.models.instance_status import InstanceStatus


def get_api_client(
    api_token: Optional[str] = None, host: Optional[str] = None
) -> tuple[AppsApi, ServicesApi, InstancesApi]:
    """
    Get configured API clients for Koyeb operations.

    Args:
        api_token: Koyeb API token. If not provided, will try to get from KOYEB_API_TOKEN env var
        host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)

    Returns:
        Tuple of (AppsApi, ServicesApi, InstancesApi) instances

    Raises:
        ValueError: If API token is not provided
    """
    token = api_token or os.getenv("KOYEB_API_TOKEN")
    if not token:
        raise ValueError(
            "API token is required. Set KOYEB_API_TOKEN environment variable or pass api_token parameter"
        )

    api_host = host or os.getenv("KOYEB_API_HOST", "https://app.koyeb.com")
    configuration = Configuration(host=api_host)
    configuration.api_key["Bearer"] = token
    configuration.api_key_prefix["Bearer"] = "Bearer"

    api_client = ApiClient(configuration)
    return AppsApi(api_client), ServicesApi(api_client), InstancesApi(api_client)


def build_env_vars(env: Optional[Dict[str, str]]) -> List[DeploymentEnv]:
    """
    Build environment variables list from dictionary.

    Args:
        env: Dictionary of environment variables

    Returns:
        List of DeploymentEnv objects
    """
    env_vars = []
    if env:
        for key, value in env.items():
            env_vars.append(DeploymentEnv(key=key, value=value))
    return env_vars


def create_docker_source(image: str, command_args: List[str]) -> DockerSource:
    """
    Create Docker source configuration.

    Args:
        image: Docker image name
        command_args: Command and arguments to run

    Returns:
        DockerSource object
    """
    return DockerSource(
        image=image,
        command=command_args[0] if command_args else None,
        args=list(command_args[1:]) if len(command_args) > 1 else None,
    )


def create_deployment_definition(
    name: str,
    docker_source: DockerSource,
    env_vars: List[DeploymentEnv],
    instance_type: str,
    ports: Optional[List[DeploymentPort]] = None,
    regions: List[str] = None,
) -> DeploymentDefinition:
    """
    Create deployment definition for a sandbox service.

    Args:
        name: Service name
        docker_source: Docker configuration
        env_vars: Environment variables
        instance_type: Instance type
        ports: List of ports (if provided, type becomes WEB, otherwise WORKER)
        regions: List of regions (defaults to North America)

    Returns:
        DeploymentDefinition object
    """
    if regions is None:
        regions = ["na"]

    deployment_type = (
        DeploymentDefinitionType.WEB if ports else DeploymentDefinitionType.WORKER
    )

    return DeploymentDefinition(
        name=name,
        type=deployment_type,
        docker=docker_source,
        env=env_vars,
        ports=ports,
        instance_types=[DeploymentInstanceType(type=instance_type)],
        scalings=[DeploymentScaling(min=1, max=1)],
        regions=regions,
    )


def get_sandbox_status(
    instance_id: str, api_token: Optional[str] = None
) -> InstanceStatus:
    """Get the current status of a sandbox instance."""
    try:
        _, _, instances_api = get_api_client(api_token)
        instance_response = instances_api.get_instance(instance_id)
        return instance_response.instance.status
    except (NotFoundException, ApiException, Exception):
        return InstanceStatus.ERROR


def is_sandbox_healthy(instance_id: str, api_token: Optional[str] = None) -> bool:
    """Check if sandbox is healthy and ready for operations."""
    return get_sandbox_status(instance_id, api_token) == InstanceStatus.HEALTHY


def ensure_sandbox_healthy(instance_id: str, api_token: Optional[str] = None) -> None:
    """Ensure a sandbox instance is healthy, raising an exception if not."""
    status = get_sandbox_status(instance_id, api_token)

    if status == InstanceStatus.ERROR:
        raise SandboxError("Sandbox is in error state")
    elif status in [InstanceStatus.STOPPING, InstanceStatus.STOPPED]:
        raise SandboxError(f"Sandbox is {status.value}, cannot perform operations")
    elif status != InstanceStatus.HEALTHY:
        raise SandboxError(f"Sandbox is not healthy (status: {status.value})")


class SandboxError(Exception):
    """Base exception for sandbox operations"""
