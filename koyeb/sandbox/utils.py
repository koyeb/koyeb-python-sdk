# coding: utf-8

"""
Utility functions for Koyeb Sandbox
"""

import asyncio
import logging
import os
import shlex
from typing import Any, Callable, Dict, List, Literal, Optional, TypedDict, Union

from koyeb.api import ApiClient, Configuration
from koyeb.api.api import AppsApi, CatalogInstancesApi, InstancesApi, ServicesApi
from koyeb.api.exceptions import ApiException, NotFoundException
from koyeb.api.models.deployment_definition import DeploymentDefinition
from koyeb.api.models.deployment_definition_type import DeploymentDefinitionType
from koyeb.api.models.deployment_env import DeploymentEnv
from koyeb.api.models.deployment_instance_type import DeploymentInstanceType
from koyeb.api.models.deployment_port import DeploymentPort
from koyeb.api.models.deployment_proxy_port import DeploymentProxyPort
from koyeb.api.models.deployment_route import DeploymentRoute
from koyeb.api.models.deployment_scaling import DeploymentScaling
from koyeb.api.models.deployment_scaling_target import DeploymentScalingTarget
from koyeb.api.models.deployment_scaling_target_sleep_idle_delay import (
    DeploymentScalingTargetSleepIdleDelay,
)
from koyeb.api.models.docker_source import DockerSource
from koyeb.api.models.instance_status import InstanceStatus
from koyeb.api.models.proxy_port_protocol import ProxyPortProtocol

# Setup logging
logger = logging.getLogger(__name__)

# Constants
MIN_PORT = 1
MAX_PORT = 65535
DEFAULT_INSTANCE_WAIT_TIMEOUT = 60  # seconds
DEFAULT_POLL_INTERVAL = 2.0  # seconds
DEFAULT_COMMAND_TIMEOUT = 30  # seconds
DEFAULT_HTTP_TIMEOUT = 30  # seconds for HTTP requests

# Error messages
ERROR_MESSAGES = {
    "NO_SUCH_FILE": ["No such file", "not found", "No such file or directory"],
    "FILE_EXISTS": ["exists", "already exists"],
    "DIR_NOT_EMPTY": ["not empty", "Directory not empty"],
}

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


def create_docker_source(
    image: str, command_args: List[str], privileged: Optional[bool] = None
) -> DockerSource:
    """
    Create Docker source configuration.

    Args:
        image: Docker image name
        command_args: Command and arguments to run (optional, empty list means use image default)
        privileged: If True, run the container in privileged mode (default: None/False)

    Returns:
        DockerSource object
    """
    return DockerSource(
        image=image,
        command=command_args[0] if command_args else None,
        args=list(command_args[1:]) if len(command_args) > 1 else None,
        privileged=privileged,
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


def create_koyeb_sandbox_proxy_ports() -> List[DeploymentProxyPort]:
    """
    Create TCP proxy port configuration for koyeb/sandbox image.

    Creates proxy port for direct TCP access:
    - Port 3031 exposed via TCP proxy

    Returns:
        List of DeploymentProxyPort objects configured for TCP proxy access
    """
    return [
        DeploymentProxyPort(
            port=3031,
            protocol=ProxyPortProtocol.TCP,
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


def create_deployment_definition(
    name: str,
    docker_source: DockerSource,
    env_vars: List[DeploymentEnv],
    instance_type: str,
    exposed_port_protocol: Optional[str] = None,
    region: Optional[str] = None,
    routes: Optional[List[DeploymentRoute]] = None,
    idle_timeout: Optional[IdleTimeout] = 300,
    enable_tcp_proxy: bool = False,
    _experimental_enable_light_sleep: bool = False,
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
        region: Region to deploy to (defaults to "na")
        routes: List of routes for public access
        idle_timeout: Number of seconds to wait before sleeping the instance if it receives no traffic
        enable_tcp_proxy: If True, enables TCP proxy for direct TCP access to port 3031
        _experimental_enable_light_sleep: If True, uses light sleep when reaching idle_timeout.
            Light Sleep reduces cold starts to ~200ms. After scaling to zero, the service stays in Light Sleep for 3600s before going into Deep Sleep.

    Returns:
        DeploymentDefinition object
    """
    if region is None:
        region = "na"

    # Convert single region string to list for API
    regions_list = [region]

    # Always create ports with protocol (default to "http" if not specified)
    protocol = exposed_port_protocol if exposed_port_protocol is not None else "http"
    # Validate protocol using API model structure
    protocol = _validate_port_protocol(protocol)
    ports = create_koyeb_sandbox_ports(protocol)

    # Create TCP proxy ports if enabled
    proxy_ports = None
    if enable_tcp_proxy:
        proxy_ports = create_koyeb_sandbox_proxy_ports()

    # Always use SANDBOX type
    deployment_type = DeploymentDefinitionType.SANDBOX

    # Process idle_timeout
    if idle_timeout is None or idle_timeout == 0:
        sleep_idle_delay = None
    elif _experimental_enable_light_sleep:
        # Experimental mode: idle_timeout sets light_sleep value, deep_sleep is always 3900
        sleep_idle_delay = DeploymentScalingTargetSleepIdleDelay(
            light_sleep_value=idle_timeout,
            deep_sleep_value=3900,
        )
    else:
        # Normal mode: only use deep_sleep
        sleep_idle_delay = DeploymentScalingTargetSleepIdleDelay(
            deep_sleep_value=idle_timeout,
        )

    # Create scaling configuration
    # If idle_timeout is 0, explicitly disable scale-to-zero (min=1, always-on)
    # Otherwise (None or int > 0), enable scale-to-zero (min=0)
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
        proxy_ports=proxy_ports,
        routes=routes,
        instance_types=[DeploymentInstanceType(type=instance_type)],
        scalings=scalings,
        regions=regions_list,
    )


def get_sandbox_status(
    instance_id: str, api_token: Optional[str] = None
) -> InstanceStatus:
    """Get the current status of a sandbox instance."""
    try:
        _, _, instances_api, _ = get_api_client(api_token)
        instance_response = instances_api.get_instance(instance_id)
        return instance_response.instance.status
    except (NotFoundException, ApiException) as e:
        logger.debug(f"Failed to get sandbox status: {e}")
        return InstanceStatus.ERROR
    except Exception as e:
        logger.warning(f"Unexpected error getting sandbox status: {e}")
        return InstanceStatus.ERROR


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
        from .executor_client import SandboxClient

        client = SandboxClient(sandbox_url, sandbox_secret)
        health_response = client.health()
        # Check if health response indicates the server is healthy
        # The exact response format may vary, but typically has a "status" field
        if isinstance(health_response, dict):
            status = health_response.get("status", "").lower()
            is_healthy = status in ["ok", "healthy", "ready"]
            if not is_healthy:
                logger.debug(f"Sandbox executor health check returned status: {status}")
            return is_healthy
        return True  # If we got a response, consider it healthy
    except Exception as e:
        # If we can't reach the executor API, consider it unhealthy
        logger.debug(f"Sandbox executor health check failed: {e}")
        return False


def escape_shell_arg(arg: str) -> str:
    """
    Escape a shell argument for safe use in shell commands.

    Args:
        arg: The argument to escape

    Returns:
        Properly escaped shell argument
    """
    return shlex.quote(arg)


def validate_port(port: int) -> None:
    """
    Validate that a port number is in the valid range.

    Args:
        port: Port number to validate

    Raises:
        ValueError: If port is not in valid range [1, 65535]
    """
    if not isinstance(port, int) or port < MIN_PORT or port > MAX_PORT:
        raise ValueError(
            f"Port must be an integer between {MIN_PORT} and {MAX_PORT}, got {port}"
        )


def check_error_message(error_msg: str, error_type: str) -> bool:
    """
    Check if an error message matches a specific error type.
    Uses case-insensitive matching against known error patterns.

    Args:
        error_msg: The error message to check
        error_type: The type of error to check for (key in ERROR_MESSAGES)

    Returns:
        True if error message matches the error type
    """
    if error_type not in ERROR_MESSAGES:
        return False

    error_msg_lower = error_msg.lower()
    patterns = ERROR_MESSAGES[error_type]
    return any(pattern.lower() in error_msg_lower for pattern in patterns)


async def run_sync_in_executor(
    method: Callable[..., Any], *args: Any, **kwargs: Any
) -> Any:
    """
    Run a synchronous method in an async executor.

    Helper function to wrap synchronous methods for async execution.
    Used by AsyncSandbox and AsyncSandboxFilesystem to wrap sync parent methods.

    Args:
        method: The synchronous method to run
        *args: Positional arguments for the method
        **kwargs: Keyword arguments for the method

    Returns:
        Result of the synchronous method call
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: method(*args, **kwargs))


def async_wrapper(method_name: str):
    """
    Decorator to automatically create async wrapper for sync methods.

    This decorator creates an async method that wraps a sync method from the parent class.
    The sync method is called via super() and executed in an executor.

    Args:
        method_name: Name of the sync method to wrap (from parent class)

    Usage:
        @async_wrapper("delete")
        async def delete(self) -> None:
            \"\"\"Delete the sandbox instance asynchronously.\"\"\"
            pass  # Implementation is handled by decorator
    """

    def decorator(func):
        async def wrapper(self, *args, **kwargs):
            # Get the parent class from MRO (Method Resolution Order)
            # __mro__[0] is the current class, __mro__[1] is the parent
            parent_class = self.__class__.__mro__[1]
            # Get the unbound method from parent class
            sync_method = getattr(parent_class, method_name)
            # Bind it to self (equivalent to super().method_name)
            bound_method = sync_method.__get__(self, parent_class)
            return await self._run_sync(bound_method, *args, **kwargs)

        # Preserve function metadata
        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__doc__ = func.__doc__ or f"{method_name} (async version)"
        wrapper.__annotations__ = func.__annotations__
        return wrapper

    return decorator


def create_sandbox_client(
    sandbox_url: Optional[str],
    sandbox_secret: Optional[str],
    existing_client: Optional[Any] = None,
) -> Any:
    """
    Create or return existing SandboxClient instance with validation.

    Helper function to create SandboxClient instances with consistent validation.
    Used by Sandbox, SandboxExecutor, and SandboxFilesystem to avoid duplication.

    Args:
        sandbox_url: The sandbox URL (from _get_sandbox_url() or sandbox._get_sandbox_url())
        sandbox_secret: The sandbox secret
        existing_client: Existing client instance to return if not None

    Returns:
        SandboxClient: Configured client instance

    Raises:
        SandboxError: If sandbox URL or secret is not available
    """
    if existing_client is not None:
        return existing_client

    if not sandbox_url:
        raise SandboxError("Unable to get sandbox URL")
    if not sandbox_secret:
        raise SandboxError("Sandbox secret not available")

    from .executor_client import SandboxClient

    return SandboxClient(sandbox_url, sandbox_secret)


class SandboxError(Exception):
    """Base exception for sandbox operations"""


class SandboxTimeoutError(SandboxError):
    """Raised when a sandbox operation times out"""
