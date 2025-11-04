# coding: utf-8

"""
Utility functions for Koyeb Sandbox
"""

import os
from typing import Dict, List, Literal, Optional, TypedDict, Union

from koyeb.api import ApiClient, Configuration
from koyeb.api.api import AppsApi, CatalogInstancesApi, InstancesApi, ServicesApi
from koyeb.api.exceptions import ApiException, NotFoundException
from koyeb.api.models.deployment_definition import DeploymentDefinition
from koyeb.api.models.deployment_definition_type import DeploymentDefinitionType
from koyeb.api.models.deployment_env import DeploymentEnv
from koyeb.api.models.deployment_instance_type import DeploymentInstanceType
from koyeb.api.models.deployment_port import DeploymentPort
from koyeb.api.models.deployment_route import DeploymentRoute
from koyeb.api.models.deployment_scaling import DeploymentScaling
from koyeb.api.models.deployment_scaling_target import DeploymentScalingTarget
from koyeb.api.models.deployment_scaling_target_sleep_idle_delay import (
    DeploymentScalingTargetSleepIdleDelay,
)
from koyeb.api.models.docker_source import DockerSource
from koyeb.api.models.instance_status import InstanceStatus

from .executor_client import SandboxClient

# Type definitions for idle timeout
IdleTimeoutSeconds = int


class IdleTimeoutConfig(TypedDict, total=False):
    """Configuration for idle timeout with light and deep sleep."""

    light_sleep: IdleTimeoutSeconds  # Optional, but if provided, deep_sleep is required
    deep_sleep: IdleTimeoutSeconds  # Required


IdleTimeout = Union[
    Literal[0],  # Disable scale-to-zero
    IdleTimeoutSeconds,  # Deep sleep only (standard and GPU instances)
    IdleTimeoutConfig,  # Explicit light_sleep/deep_sleep configuration
]

# Valid protocols for DeploymentPort (from OpenAPI spec: http, http2, tcp)
# For sandboxes, we only support http and http2
VALID_DEPLOYMENT_PORT_PROTOCOLS = ("http", "http2")


def _validate_port_protocol(protocol: str) -> str:
    """
    Validate port protocol using API model structure.

    Args:
        protocol: Protocol string to validate

    Returns:
        Validated protocol string

    Raises:
        ValueError: If protocol is invalid
    """
    # Validate by attempting to create a DeploymentPort instance
    # This ensures we're using the API model's validation structure
    try:
        port = DeploymentPort(port=3030, protocol=protocol)
        # Additional validation: check if protocol is in allowed values
        if protocol not in VALID_DEPLOYMENT_PORT_PROTOCOLS:
            raise ValueError(
                f"Invalid protocol '{protocol}'. Must be one of {VALID_DEPLOYMENT_PORT_PROTOCOLS}"
            )
        return port.protocol or "http"
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(
            f"Invalid protocol '{protocol}'. Must be one of {VALID_DEPLOYMENT_PORT_PROTOCOLS}"
        ) from e


def get_api_client(
    api_token: Optional[str] = None, host: Optional[str] = None
) -> tuple[AppsApi, ServicesApi, InstancesApi, CatalogInstancesApi]:
    """
    Get configured API clients for Koyeb operations.

    Args:
        api_token: Koyeb API token. If not provided, will try to get from KOYEB_API_TOKEN env var
        host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)

    Returns:
        Tuple of (AppsApi, ServicesApi, InstancesApi, CatalogInstancesApi) instances

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
    return (
        AppsApi(api_client),
        ServicesApi(api_client),
        InstancesApi(api_client),
        CatalogInstancesApi(api_client),
    )


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


def create_koyeb_sandbox_ports(protocol: str = "http") -> List[DeploymentPort]:
    """
    Create port configuration for koyeb/sandbox image.

    Creates two ports:
    - Port 3030 exposed on HTTP, mounted on /koyeb-sandbox/
    - Port 3031 exposed with the specified protocol, mounted on /

    Args:
        protocol: Protocol to use for port 3031 ("http" or "http2"), defaults to "http"

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
            protocol=protocol,
        ),
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
        DeploymentRoute(port=3030, path="/koyeb-sandbox/"),
        DeploymentRoute(port=3031, path="/"),
    ]


def _validate_idle_timeout(idle_timeout: Optional[IdleTimeout]) -> None:
    """
    Validate idle_timeout parameter according to spec.

    Raises:
        ValueError: If validation fails
    """
    if idle_timeout is None:
        return

    if isinstance(idle_timeout, int):
        if idle_timeout < 0:
            raise ValueError("idle_timeout must be >= 0")
        if idle_timeout > 0:
            # Deep sleep only - valid
            return
        # idle_timeout == 0 means disable scale-to-zero - valid
        return

    if isinstance(idle_timeout, dict):
        if "deep_sleep" not in idle_timeout:
            raise ValueError(
                "idle_timeout dict must contain 'deep_sleep' key (at minimum)"
            )

        deep_sleep = idle_timeout.get("deep_sleep")
        if deep_sleep is None or not isinstance(deep_sleep, int) or deep_sleep <= 0:
            raise ValueError("deep_sleep must be a positive integer")

        if "light_sleep" in idle_timeout:
            light_sleep = idle_timeout.get("light_sleep")
            if (
                light_sleep is None
                or not isinstance(light_sleep, int)
                or light_sleep <= 0
            ):
                raise ValueError("light_sleep must be a positive integer")

            if deep_sleep < light_sleep:
                raise ValueError(
                    "deep_sleep must be >= light_sleep when both are provided"
                )


def _is_light_sleep_enabled(
    instance_type: str,
    catalog_instances_api: Optional[CatalogInstancesApi] = None,
) -> bool:
    """
    Check if light sleep is enabled for the instance type using API or fallback.

    Args:
        instance_type: Instance type string
        catalog_instances_api: Optional CatalogInstancesApi client (if None, will try to create one)

    Returns:
        True if light sleep is enabled, False otherwise (defaults to True if API call fails)
    """
    try:
        if catalog_instances_api is None:
            _, _, _, catalog_instances_api = get_api_client(None)
        response = catalog_instances_api.get_catalog_instance(id=instance_type)
        if response and response.instance:
            return response.instance.light_sleep_enabled or False
    except (ApiException, NotFoundException):
        # If API call fails, default to True (assume light sleep is enabled)
        pass
    except Exception:
        # Any other error, default to True (assume light sleep is enabled)
        pass
    # Default to True if we can't determine from API
    return True


def _process_idle_timeout(
    idle_timeout: Optional[IdleTimeout],
    light_sleep_enabled: bool = True,
) -> Optional[DeploymentScalingTargetSleepIdleDelay]:
    """
    Process idle_timeout parameter and convert to DeploymentScalingTargetSleepIdleDelay.

    According to spec:
    - If unsupported instance type: idle_timeout is silently ignored (returns None)
    - None (default): Auto-enable light_sleep=300s, deep_sleep=600s
    - 0: Explicitly disable scale-to-zero (returns None)
    - int > 0: Deep sleep only
    - dict: Explicit configuration
    - If light_sleep_enabled is False for the instance type, light_sleep is ignored

    Args:
        idle_timeout: Idle timeout configuration
        light_sleep_enabled: Whether light sleep is enabled for the instance type (default: True)

    Returns:
        DeploymentScalingTargetSleepIdleDelay or None if disabled/ignored
    """
    # Validate the parameter
    _validate_idle_timeout(idle_timeout)

    # Process according to spec
    if idle_timeout is None:
        # Default: Auto-enable light_sleep=300s, deep_sleep=600s
        # If light sleep is not enabled, only use deep_sleep
        if not light_sleep_enabled:
            return DeploymentScalingTargetSleepIdleDelay(
                deep_sleep_value=600,
            )
        return DeploymentScalingTargetSleepIdleDelay(
            light_sleep_value=300,
            deep_sleep_value=600,
        )

    if isinstance(idle_timeout, int):
        if idle_timeout == 0:
            # Explicitly disable scale-to-zero
            return None
        # Deep sleep only
        return DeploymentScalingTargetSleepIdleDelay(
            deep_sleep_value=idle_timeout,
        )

    if isinstance(idle_timeout, dict):
        deep_sleep = idle_timeout.get("deep_sleep")
        light_sleep = idle_timeout.get("light_sleep")

        # If light sleep is not enabled, ignore light_sleep if provided
        if not light_sleep_enabled:
            return DeploymentScalingTargetSleepIdleDelay(
                deep_sleep_value=deep_sleep,
            )

        if light_sleep is not None:
            # Both light_sleep and deep_sleep provided
            return DeploymentScalingTargetSleepIdleDelay(
                light_sleep_value=light_sleep,
                deep_sleep_value=deep_sleep,
            )
        else:
            # Deep sleep only
            return DeploymentScalingTargetSleepIdleDelay(
                deep_sleep_value=deep_sleep,
            )


def create_deployment_definition(
    name: str,
    docker_source: DockerSource,
    env_vars: List[DeploymentEnv],
    instance_type: str,
    exposed_port_protocol: Optional[str] = None,
    regions: List[str] = None,
    routes: Optional[List[DeploymentRoute]] = None,
    idle_timeout: Optional[IdleTimeout] = None,
    light_sleep_enabled: bool = True,
) -> DeploymentDefinition:
    """
    Create deployment definition for a sandbox service.

    Args:
        name: Service name
        docker_source: Docker configuration
        env_vars: Environment variables
        instance_type: Instance type
        exposed_port_protocol: Protocol to expose ports with ("http" or "http2").
            If None, defaults to "http".
            If provided, must be one of "http" or "http2".
        regions: List of regions (defaults to ["na"])
        routes: List of routes for public access
        idle_timeout: Idle timeout configuration (see IdleTimeout type)
        light_sleep_enabled: Whether light sleep is enabled for the instance type (default: True)

    Returns:
        DeploymentDefinition object
    """
    if regions is None:
        regions = ["na"]

    # Always create ports with protocol (default to "http" if not specified)
    protocol = exposed_port_protocol if exposed_port_protocol is not None else "http"
    # Validate protocol using API model structure
    protocol = _validate_port_protocol(protocol)
    ports = create_koyeb_sandbox_ports(protocol)

    # Always use WEB type
    deployment_type = DeploymentDefinitionType.WEB

    # Process idle_timeout
    sleep_idle_delay = _process_idle_timeout(idle_timeout, light_sleep_enabled)

    # Create scaling configuration
    # If idle_timeout is 0, explicitly disable scale-to-zero (min=1, always-on)
    # Otherwise (None, int > 0, or dict), enable scale-to-zero (min=0)
    min_scale = 1 if idle_timeout == 0 else 0
    targets = None
    if sleep_idle_delay is not None:
        scaling_target = DeploymentScalingTarget(sleep_idle_delay=sleep_idle_delay)
        targets = [scaling_target]

    scalings = [DeploymentScaling(min=min_scale, max=1, targets=targets)]

    return DeploymentDefinition(
        name=name,
        type=deployment_type,
        docker=docker_source,
        env=env_vars,
        ports=ports,
        routes=routes,
        instance_types=[DeploymentInstanceType(type=instance_type)],
        scalings=scalings,
        regions=regions,
    )


def get_sandbox_status(
    instance_id: str, api_token: Optional[str] = None
) -> InstanceStatus:
    """Get the current status of a sandbox instance."""
    try:
        _, _, instances_api, _ = get_api_client(api_token)
        instance_response = instances_api.get_instance(instance_id)
        return instance_response.instance.status
    except (NotFoundException, ApiException, Exception):
        return InstanceStatus.ERROR


def _get_sandbox_domain(
    service_id: str, api_token: Optional[str] = None
) -> Optional[str]:
    """
    Internal function to get the public domain of a sandbox service.

    Returns the domain name (e.g., "app-name-org.koyeb.app") without protocol or path.

    Args:
        service_id: The service ID
        api_token: Optional API token (if None, will try to get from KOYEB_API_TOKEN env var)

    Returns:
        Optional[str]: The domain name or None if unavailable
    """
    try:
        _, services_api, _, _ = get_api_client(api_token)
        service_response = services_api.get_service(service_id)
        service = service_response.service

        if service.app_id:
            apps_api, _, _, _ = get_api_client(api_token)
            app_response = apps_api.get_app(service.app_id)
            app = app_response.app
            if hasattr(app, "domains") and app.domains:
                # Use the first public domain
                return app.domains[0].name
        return None
    except (NotFoundException, ApiException, Exception):
        return None


def is_sandbox_healthy(
    instance_id: str,
    sandbox_url: str,
    sandbox_secret: str,
    api_token: Optional[str] = None,
) -> bool:
    """
    Check if sandbox is healthy and ready for operations.

    This function requires both sandbox_url and sandbox_secret to properly check:
    1. The Koyeb instance status (via API) - using instance_id and api_token
    2. The sandbox executor health endpoint (via SandboxClient) - using sandbox_url and sandbox_secret

    Args:
        instance_id: The Koyeb instance ID
        api_token: Koyeb API token
        sandbox_url: URL of the sandbox executor API (required)
        sandbox_secret: Secret for sandbox executor authentication (required)

    Returns:
        bool: True if sandbox is healthy, False otherwise

    Raises:
        ValueError: If sandbox_url or sandbox_secret are not provided
    """
    if not sandbox_url:
        raise ValueError("sandbox_url is required for health check")
    if not sandbox_secret:
        raise ValueError("sandbox_secret is required for health check")

    # Check Koyeb instance status
    instance_healthy = (
        get_sandbox_status(instance_id, api_token) == InstanceStatus.HEALTHY
    )

    # If instance is not healthy, no need to check executor
    if not instance_healthy:
        return False

    # Check executor health
    try:
        client = SandboxClient(sandbox_url, sandbox_secret)
        health_response = client.health()
        # Check if health response indicates the server is healthy
        # The exact response format may vary, but typically has a "status" field
        if isinstance(health_response, dict):
            status = health_response.get("status", "").lower()
            return status in ["ok", "healthy", "ready"]
        return True  # If we got a response, consider it healthy
    except Exception:
        # If we can't reach the executor API, consider it unhealthy
        return False


class SandboxError(Exception):
    """Base exception for sandbox operations"""
