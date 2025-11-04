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
from koyeb.api.models.deployment_route import DeploymentRoute
from koyeb.api.models.deployment_scaling import DeploymentScaling
from koyeb.api.models.docker_source import DockerSource
from koyeb.api.models.instance_status import InstanceStatus

from .executor_client import SandboxClient


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
        command_args: Command and arguments to run (optional, empty list means use image default)

    Returns:
        DockerSource object
    """
    return DockerSource(
        image=image,
        command=command_args[0] if command_args else None,
        args=list(command_args[1:]) if len(command_args) > 1 else None,
    )


def create_koyeb_sandbox_ports() -> List[DeploymentPort]:
    """
    Create port configuration for koyeb/sandbox image.
    
    Creates two ports:
    - Port 3030 exposed on HTTP, mounted on /koyeb-sandbox/
    - Port 3031 exposed on HTTP, mounted on /
    
    Returns:
        List of DeploymentPort objects configured for koyeb/sandbox
    """
    return [
        DeploymentPort(
            port=3030,
            protocol="http",
        ),
        DeploymentPort(
            port=3031,
            protocol="http",
        )
    ]


def create_koyeb_sandbox_routes() -> List[DeploymentRoute]:
    """
    Create route configuration for koyeb/sandbox image to make it publicly accessible.
    
    Creates two routes:
    - Port 3030 accessible at /koyeb-sandbox/
    - Port 3031 accessible at /
    
    Returns:
        List of DeploymentRoute objects configured for koyeb/sandbox
    """
    return [
        DeploymentRoute(
            port=3030,
            path="/koyeb-sandbox/"
        ),
        DeploymentRoute(
            port=3031,
            path="/"
        )
    ]


def create_deployment_definition(
    name: str,
    docker_source: DockerSource,
    env_vars: List[DeploymentEnv],
    instance_type: str,
    ports: Optional[List[DeploymentPort]] = None,
    regions: List[str] = None,
    routes: Optional[List[DeploymentRoute]] = None,
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
        routes: List of routes for public access

    Returns:
        DeploymentDefinition object
    """
    if regions is None:
        regions = ["eu"]

    deployment_type = (
        DeploymentDefinitionType.WEB if ports else DeploymentDefinitionType.WORKER
    )

    return DeploymentDefinition(
        name=name,
        type=deployment_type,
        docker=docker_source,
        env=env_vars,
        ports=ports,
        routes=routes,
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


def get_sandbox_url(service_id: str, api_token: Optional[str] = None) -> Optional[str]:
    """
    Get the public URL of a sandbox service.
    
    Returns the URL with /koyeb-sandbox path prepended since the sandbox
    executor API is exposed on port 3030 which is mounted at /koyeb-sandbox/.
    """
    try:
        _, services_api, _ = get_api_client(api_token)
        service_response = services_api.get_service(service_id)
        
        # Get the service app URL (this would be like: app-name-org.koyeb.app)
        # The URL is typically constructed from the app name and organization
        service = service_response.service
        if hasattr(service, 'app_url') and service.app_url:
            return f"https://{service.app_url}/koyeb-sandbox"
        
        # If app_url is not available, we need to get it from the app
        if service.app_id:
            apps_api, _, _ = get_api_client(api_token)
            app_response = apps_api.get_app(service.app_id)
            app = app_response.app
            if hasattr(app, 'domains') and app.domains:
                # Use the first public domain
                return f"https://{app.domains[0]}/koyeb-sandbox"
            # Fallback: construct from app name
            if app.name and service.organization_id:
                # This is an approximation - actual URL construction may vary
                return f"https://{app.name}.koyeb.app/koyeb-sandbox"
        
        return None
    except (NotFoundException, ApiException, Exception):
        return None


def is_sandbox_healthy(
    instance_id: str, 
    api_token: Optional[str] = None,
    sandbox_url: Optional[str] = None,
    sandbox_secret: Optional[str] = None
) -> bool:
    """
    Check if sandbox is healthy and ready for operations.
    
    This function checks both:
    1. The Koyeb instance status (via API)
    2. The sandbox executor health endpoint (via SandboxClient, if URL and secret are provided)
    
    Args:
        instance_id: The Koyeb instance ID
        api_token: Koyeb API token
        sandbox_url: Optional URL of the sandbox executor API
        sandbox_secret: Optional secret for sandbox executor authentication
        
    Returns:
        bool: True if sandbox is healthy, False otherwise
    """
    # Check Koyeb instance status
    instance_healthy = get_sandbox_status(instance_id, api_token) == InstanceStatus.HEALTHY
    
    # If instance is not healthy, no need to check executor
    if not instance_healthy:
        return False
    
    # If sandbox URL and secret are provided, also check executor health
    if sandbox_url and sandbox_secret:
        try:
            client = SandboxClient(sandbox_url, sandbox_secret)
            health_response = client.health()
            # Check if health response indicates the server is healthy
            # The exact response format may vary, but typically has a "status" field
            if isinstance(health_response, dict):
                status = health_response.get('status', '').lower()
                return status in ['ok', 'healthy', 'ready']
            return True  # If we got a response, consider it healthy
        except Exception:
            # If we can't reach the executor API, consider it unhealthy
            return False
    
    # If only instance status was checked, return that result
    return instance_healthy


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
