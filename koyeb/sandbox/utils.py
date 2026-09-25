# coding: utf-8

"""
Utility functions for Koyeb Sandbox
"""

import ipaddress
import logging
import os
import shlex
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from koyeb.api import ApiClient, Configuration
from koyeb.api.api import (
    AppsApi,
    CatalogInstancesApi,
    DeploymentsApi,
    InstancesApi,
    InstanceSnapshotsApi,
    PoolClaimsApi,
    SecretsApi,
    ServicePoolsApi,
    ServicesApi,
)
from koyeb.api.models.deployment_status import DeploymentStatus
from koyeb.api.models.service_status import ServiceStatus
from koyeb.api.models.egress_policy import EgressPolicy
from koyeb.api.models.egress_policy_mode import EgressPolicyMode
from koyeb.api.models.network_policy import NetworkPolicy
from koyeb.api.models.network_policy_destination import NetworkPolicyDestination

# Setup logging
logger = logging.getLogger(__name__)

# Constants
MIN_PORT = 1
MAX_PORT = 65535
DEFAULT_INSTANCE_WAIT_TIMEOUT = 60  # seconds
DEFAULT_POLL_INTERVAL = 0.5  # seconds
DEFAULT_COMMAND_TIMEOUT = 30  # seconds
DEFAULT_HTTP_TIMEOUT = 30  # seconds for HTTP requests

# Error messages
ERROR_MESSAGES = {
    "NO_SUCH_FILE": ["No such file", "not found", "No such file or directory"],
    "FILE_EXISTS": ["exists", "already exists"],
    "DIR_NOT_EMPTY": ["not empty", "Directory not empty"],
}

StatusClassification = Literal["ready", "in_progress", "terminal_failure"]


def classify_service_status(status: Union[ServiceStatus, str]) -> StatusClassification:
    """Classify a service status for readiness, failing closed.

    HEALTHY and DEGRADED are usable, STARTING and RESUMING are still in
    progress, and every other state — including unknown forward-compat
    values — is a terminal failure. Mirrors the JS SDK's
    classifyServiceStatus (src/claim.ts).
    """
    if status in (ServiceStatus.HEALTHY, ServiceStatus.DEGRADED):
        return "ready"
    if status in (ServiceStatus.STARTING, ServiceStatus.RESUMING):
        return "in_progress"
    return "terminal_failure"


def classify_deployment_status(
    status: Union[DeploymentStatus, str],
) -> StatusClassification:
    """Classify a deployment status for readiness, failing closed.

    HEALTHY and DEGRADED are ready, the pre-ready states (PENDING,
    PROVISIONING, SCHEDULED, ALLOCATING, STARTING) are in progress, and every
    other state — including SLEEPING, STASHED, and unknown forward-compat
    values — is terminal: it will not become ready on its own during a wait.
    """
    if status in (DeploymentStatus.HEALTHY, DeploymentStatus.DEGRADED):
        return "ready"
    if status in (
        DeploymentStatus.PENDING,
        DeploymentStatus.PROVISIONING,
        DeploymentStatus.SCHEDULED,
        DeploymentStatus.ALLOCATING,
        DeploymentStatus.STARTING,
    ):
        return "in_progress"
    return "terminal_failure"


@dataclass(frozen=True)
class ApiClients:
    """Bundle of Koyeb API clients sharing a single underlying ApiClient."""

    apps: AppsApi
    services: ServicesApi
    instances: InstancesApi
    catalog_instances: CatalogInstancesApi
    deployments: DeploymentsApi
    secrets: SecretsApi
    instance_snapshots: Any
    service_pools: ServicePoolsApi
    pool_claims: PoolClaimsApi


_api_clients_cache: Dict[Tuple[str, str], ApiClients] = {}


def get_api_clients(
    api_token: Optional[str] = None, host: Optional[str] = None
) -> ApiClients:
    """
    Get configured API clients for Koyeb operations.

    Caches clients by (token, host) to reuse the underlying HTTP connection pool.

    Args:
        api_token: Koyeb API token. If not provided, will try to get from KOYEB_API_TOKEN env var
        host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)

    Returns:
        ApiClients with apps, services, instances, catalog_instances, deployments, and secrets attributes

    Raises:
        ValueError: If API token is not provided
    """
    token = api_token or os.getenv("KOYEB_API_TOKEN")
    if not token:
        raise MissingApiTokenError()

    api_host = os.getenv("KOYEB_API_HOST", host)
    if not api_host:
        api_host = "https://app.koyeb.com"
    cache_key = (token, api_host)

    if cache_key in _api_clients_cache:
        return _api_clients_cache[cache_key]

    configuration = Configuration(host=api_host)
    configuration.api_key["Bearer"] = token
    configuration.api_key_prefix["Bearer"] = "Bearer"

    api_client = ApiClient(configuration)
    clients = ApiClients(
        apps=AppsApi(api_client),
        services=ServicesApi(api_client),
        instances=InstancesApi(api_client),
        catalog_instances=CatalogInstancesApi(api_client),
        deployments=DeploymentsApi(api_client),
        secrets=SecretsApi(api_client),
        instance_snapshots=InstanceSnapshotsApi(api_client),
        service_pools=ServicePoolsApi(api_client),
        pool_claims=PoolClaimsApi(api_client),
    )
    _api_clients_cache[cache_key] = clients
    return clients


# --- Async API clients ---

from koyeb.api_async import ApiClient as AsyncApiClient
from koyeb.api_async import Configuration as AsyncConfiguration
from koyeb.api_async.api import (
    AppsApi as AsyncAppsApi,
    CatalogInstancesApi as AsyncCatalogInstancesApi,
    DeploymentsApi as AsyncDeploymentsApi,
    InstancesApi as AsyncInstancesApi,
    InstanceSnapshotsApi as AsyncInstanceSnapshotsApi,
    PoolClaimsApi as AsyncPoolClaimsApi,
    SecretsApi as AsyncSecretsApi,
    ServicePoolsApi as AsyncServicePoolsApi,
    ServicesApi as AsyncServicesApi,
)


@dataclass(frozen=True)
class AsyncApiClients:
    """Bundle of async Koyeb API clients sharing a single underlying AsyncApiClient."""

    apps: AsyncAppsApi
    services: AsyncServicesApi
    instances: AsyncInstancesApi
    catalog_instances: AsyncCatalogInstancesApi
    deployments: AsyncDeploymentsApi
    secrets: AsyncSecretsApi
    instance_snapshots: Any
    service_pools: AsyncServicePoolsApi
    pool_claims: AsyncPoolClaimsApi


_async_api_clients_cache: Dict[Tuple[str, str], AsyncApiClients] = {}


def get_async_api_clients(
    api_token: Optional[str] = None, host: Optional[str] = None
) -> AsyncApiClients:
    """
    Get configured async API clients for Koyeb operations.

    Caches clients by (token, host) to reuse the underlying HTTP connection pool.

    Args:
        api_token: Koyeb API token. If not provided, will try to get from KOYEB_API_TOKEN env var
        host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var

    Returns:
        AsyncApiClients with async API client instances

    Raises:
        ValueError: If API token is not provided
    """
    token = api_token or os.getenv("KOYEB_API_TOKEN")
    if not token:
        raise MissingApiTokenError()

    api_host = os.getenv("KOYEB_API_HOST", host)
    if not api_host:
        api_host = "https://app.koyeb.com"
    cache_key = (token, api_host)

    if cache_key in _async_api_clients_cache:
        return _async_api_clients_cache[cache_key]

    configuration = AsyncConfiguration(host=api_host)
    configuration.api_key["Bearer"] = token
    configuration.api_key_prefix["Bearer"] = "Bearer"

    api_client = AsyncApiClient(configuration)
    clients = AsyncApiClients(
        apps=AsyncAppsApi(api_client),
        services=AsyncServicesApi(api_client),
        instances=AsyncInstancesApi(api_client),
        catalog_instances=AsyncCatalogInstancesApi(api_client),
        deployments=AsyncDeploymentsApi(api_client),
        secrets=AsyncSecretsApi(api_client),
        instance_snapshots=AsyncInstanceSnapshotsApi(api_client),
        service_pools=AsyncServicePoolsApi(api_client),
        pool_claims=AsyncPoolClaimsApi(api_client),
    )
    _async_api_clients_cache[cache_key] = clients
    return clients


def _normalize_destination(entry: str) -> str:
    """
    Normalize an outbound allowlist entry to a CIDR string.

    Bare IPv4 addresses become /32, bare IPv6 addresses become /128,
    CIDR notation is validated and passed through (host bits are cleared,
    e.g. "10.0.0.1/8" becomes "10.0.0.0/8").

    Raises:
        EgressPolicyError: If the entry is not a valid IP address or CIDR
    """
    value = entry.strip() if isinstance(entry, str) else ""
    if not value:
        raise EgressPolicyError(f"Invalid outbound_allowlist entry: {entry!r}")
    if "%" in value:
        raise EgressPolicyError(
            f"Invalid outbound_allowlist entry {entry!r}: "
            "expected an IP address or CIDR (scoped/zone-ID addresses are not allowed)"
        )
    try:
        if "/" in value:
            return str(ipaddress.ip_network(value, strict=False))
        address = ipaddress.ip_address(value)
    except ValueError as e:
        raise EgressPolicyError(
            f"Invalid outbound_allowlist entry {entry!r}: "
            "expected an IP address or CIDR"
        ) from e
    prefix = 32 if address.version == 4 else 128
    return f"{address}/{prefix}"


def build_network_policy(
    block_network: bool = False,
    outbound_allowlist: Optional[List[str]] = None,
) -> Optional[NetworkPolicy]:
    """
    Build a NetworkPolicy from sandbox network policy arguments.

    Args:
        block_network: If True, block all outbound network access
        outbound_allowlist: List of IPs/CIDRs allowed as outbound
            destinations; all other outbound traffic is blocked. Bare IPs
            are normalized to /32 (IPv4) or /128 (IPv6). An empty list
            blocks all outbound traffic.

    Returns:
        NetworkPolicy, or None when both arguments are unset
        (block_network=False and outbound_allowlist=None)

    Raises:
        EgressPolicyError: If both arguments are passed, or an allowlist
            entry is not a valid IP address or CIDR
    """
    if block_network and outbound_allowlist is not None:
        raise EgressPolicyError(
            "block_network and outbound_allowlist are mutually exclusive; "
            "pass at most one"
        )
    if not block_network and outbound_allowlist is None:
        return None

    allow_list = None
    if outbound_allowlist is not None:
        allow_list = [
            NetworkPolicyDestination(cidr=_normalize_destination(entry))
            for entry in outbound_allowlist
        ]
    return NetworkPolicy(
        egress=EgressPolicy(
            mode=EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL,
            allow_list=allow_list,
        )
    )


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
        raise InvalidPortError(port)


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


def create_sandbox_client(
    conn_info: Optional["ConnectionInfo"],
    existing_client: Optional[Any] = None,
) -> Any:
    """
    Create or return existing SandboxClient instance with validation.

    Helper function to create SandboxClient instances with consistent validation.
    Used by Sandbox, SandboxExecutor, and SandboxFilesystem to avoid duplication.

    Args:
        conn_info: The information needed to connect to the sandbox executor API
        existing_client: Existing client instance to return if not None

    Returns:
        SandboxClient: Configured client instance

    Raises:
        SandboxError: If sandbox URL or secret is not available
    """
    if existing_client is not None:
        return existing_client

    try:
        conn_info.validate()
    except ValueError as e:
        raise SandboxError(str(e))

    from .executor_client import SandboxClient

    return SandboxClient(conn_info)


def create_async_sandbox_client(
    conn_info: Optional["ConnectionInfo"],
    existing_client: Optional[Any] = None,
) -> Any:
    """
    Create or return existing AsyncSandboxClient instance with validation.

    Helper function to create AsyncSandboxClient instances with consistent validation.
    Used by AsyncSandbox to avoid duplication.

    Args:
        conn_info: The information needed to connect to the sandbox executor API
        existing_client: Existing client instance to return if not None

    Returns:
        AsyncSandboxClient: Configured async client instance

    Raises:
        SandboxError: If sandbox URL or secret is not available
    """
    if existing_client is not None:
        return existing_client

    try:
        conn_info.validate()
    except ValueError as e:
        raise SandboxError(str(e))

    from .executor_client import AsyncSandboxClient

    return AsyncSandboxClient(conn_info)


class SandboxError(Exception):
    """Base exception for sandbox operations"""


class MissingApiTokenError(SandboxError, ValueError):
    """Raised when no API token is provided and KOYEB_API_TOKEN is unset.

    Also inherits ValueError for back-compat with published 1.5.x callers
    that catch the old plain ValueError from the token gates.
    """

    DEFAULT_MESSAGE = (
        "API token is required. Set KOYEB_API_TOKEN environment variable "
        "or pass api_token parameter"
    )

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or self.DEFAULT_MESSAGE)


class InvalidPortError(SandboxError, ValueError):
    """Raised when a port is not an integer in [MIN_PORT, MAX_PORT].

    Also inherits ValueError for back-compat with published 1.5.x callers
    that catch the old plain ValueError from validate_port.
    """

    def __init__(self, port: Any):
        super().__init__(
            f"Port must be an integer between {MIN_PORT} and {MAX_PORT}, got {port}"
        )


class NoSandboxSecretError(SandboxError):
    """Raised when a sandbox deployment carries no SANDBOX_SECRET, so the
    executor connection cannot be established."""


class SandboxTimeoutError(SandboxError):
    """Raised when a sandbox operation times out"""


class SandboxDeploymentError(SandboxError):
    """Raised when a sandbox deployment reaches an error state"""


class SandboxRequestError(SandboxError):
    """Raised when the sandbox executor returns a non-OK HTTP response.

    Carries the HTTP status code and response body. SandboxServiceError
    (HTTP 5xx) subclasses this, so `except SandboxRequestError` catches
    every executor HTTP failure — mirroring the JS SDK's SandboxRequestError.
    """

    def __init__(
        self,
        status_code: int,
        body: Any = None,
        message: Optional[str] = None,
    ):
        self.status_code = status_code
        self.body = body
        super().__init__(
            message or f"Sandbox executor request failed: {status_code} {body}"
        )


class SandboxServiceError(SandboxRequestError):
    """Raised when the sandbox executor returns an HTTP 5xx error"""

    def __init__(self, status_code: int, message: str):
        super().__init__(
            status_code,
            body=message,
            message=f"Sandbox service error ({status_code}): {message}",
        )


class EgressPolicyError(SandboxError):
    """Raised when egress policy arguments are invalid or conflicting"""


class PoolClaimError(SandboxError):
    """Raised when claiming a sandbox from a service pool fails"""


class ServicePoolError(SandboxError):
    """Raised when a service pool operation fails"""


class ServiceTerminalStateError(SandboxError):
    """Raised when a service reaches a state that will never become ready"""

    def __init__(self, service_id: str, status: Any):
        self.service_id = service_id
        self.status = status
        status_value = getattr(status, "value", status)
        super().__init__(
            f"Service '{service_id}' reached terminal state '{status_value}' "
            f"and will not become ready."
        )
