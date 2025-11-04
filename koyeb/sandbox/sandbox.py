# coding: utf-8

"""
Koyeb Sandbox - Python SDK for creating and managing Koyeb sandboxes
"""

from __future__ import annotations

import asyncio
import os
import secrets
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, TypedDict

from koyeb.api.api.deployments_api import DeploymentsApi
from koyeb.api.models.create_app import CreateApp
from koyeb.api.models.create_service import CreateService

from .utils import (
    DEFAULT_INSTANCE_WAIT_TIMEOUT,
    DEFAULT_POLL_INTERVAL,
    IdleTimeout,
    SandboxError,
    _is_light_sleep_enabled,
    build_env_vars,
    create_deployment_definition,
    create_docker_source,
    create_koyeb_sandbox_routes,
    create_sandbox_client,
    get_api_client,
    is_sandbox_healthy,
    logger,
    run_sync_in_executor,
    validate_port,
)

if TYPE_CHECKING:
    from .exec import AsyncSandboxExecutor, SandboxExecutor
    from .executor_client import SandboxClient
    from .filesystem import AsyncSandboxFilesystem, SandboxFilesystem


class ProcessInfo(TypedDict, total=False):
    """Type definition for process information returned by list_processes."""

    id: str  # Process ID (UUID string)
    cmd: str  # The command that was executed
    status: str  # Process status (e.g., "running", "completed")
    pid: int  # OS process ID (if running)
    exit_code: int  # Exit code (if completed)
    started_at: str  # ISO 8601 timestamp when process started
    completed_at: str  # ISO 8601 timestamp when process completed (if applicable)


@dataclass
class ExposedPort:
    """Result of exposing a port via TCP proxy."""

    port: int
    exposed_at: str

    def __str__(self) -> str:
        return f"ExposedPort(port={self.port}, exposed_at='{self.exposed_at}')"


class Sandbox:
    """
    Synchronous sandbox for running code on Koyeb infrastructure.
    Provides creation and deletion functionality with proper health polling.
    """

    def __init__(
        self,
        sandbox_id: str,
        app_id: str,
        service_id: str,
        instance_id: str,
        name: Optional[str] = None,
        api_token: Optional[str] = None,
        sandbox_secret: Optional[str] = None,
    ):
        self.sandbox_id = sandbox_id
        self.app_id = app_id
        self.service_id = service_id
        self.instance_id = instance_id
        self.name = name
        self.api_token = api_token
        self.sandbox_secret = sandbox_secret
        self._created_at = time.time()
        self._sandbox_url = None
        self._client = None

    @classmethod
    def create(
        cls,
        image: str = "koyeb/sandbox",
        name: str = "quick-sandbox",
        wait_ready: bool = True,
        instance_type: str = "nano",
        exposed_port_protocol: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        regions: Optional[List[str]] = None,
        api_token: Optional[str] = None,
        timeout: int = 300,
        idle_timeout: Optional[IdleTimeout] = None,
        enable_tcp_proxy: bool = False,
    ) -> Sandbox:
        """
            Create a new sandbox instance.

            Args:
                image: Docker image to use (default: koyeb/sandbox)
                name: Name of the sandbox
                wait_ready: Wait for sandbox to be ready (default: True)
                instance_type: Instance type (default: nano)
                exposed_port_protocol: Protocol to expose ports with ("http" or "http2").
                    If None, defaults to "http".
                    If provided, must be one of "http" or "http2".
                env: Environment variables
                regions: List of regions to deploy to (default: ["na"])
                api_token: Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
                timeout: Timeout for sandbox creation in seconds
                idle_timeout: Idle timeout configuration for scale-to-zero
                    - None: Auto-enable (light_sleep=300s, deep_sleep=600s)
                    - 0: Disable scale-to-zero (keep always-on)
                    - int > 0: Deep sleep only (e.g., 600 for 600s deep sleep)
                    - dict: Explicit configuration with {"light_sleep": 300, "deep_sleep": 600}
                enable_tcp_proxy: If True, enables TCP proxy for direct TCP access to port 3031

        Returns:
                Sandbox: A new Sandbox instance
        """
        if api_token is None:
            api_token = os.getenv("KOYEB_API_TOKEN")
            if not api_token:
                raise ValueError(
                    "API token is required. Set KOYEB_API_TOKEN environment variable or pass api_token parameter"
                )

        sandbox = cls._create_sync(
            name=name,
            image=image,
            instance_type=instance_type,
            exposed_port_protocol=exposed_port_protocol,
            env=env,
            regions=regions,
            api_token=api_token,
            timeout=timeout,
            idle_timeout=idle_timeout,
            enable_tcp_proxy=enable_tcp_proxy,
        )

        if wait_ready:
            sandbox.wait_ready(timeout=timeout)

        return sandbox

    @classmethod
    def _create_sync(
        cls,
        name: str,
        image: str = "koyeb/sandbox",
        instance_type: str = "nano",
        exposed_port_protocol: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        regions: Optional[List[str]] = None,
        api_token: Optional[str] = None,
        timeout: int = 300,
        idle_timeout: Optional[IdleTimeout] = None,
        enable_tcp_proxy: bool = False,
    ) -> Sandbox:
        """
        Synchronous creation method that returns creation parameters.
        Subclasses can override to return their own type.
        """
        apps_api, services_api, _, catalog_instances_api = get_api_client(api_token)

        # Always create routes (ports are always exposed, default to "http")
        routes = create_koyeb_sandbox_routes()

        # Generate secure sandbox secret
        sandbox_secret = secrets.token_urlsafe(32)

        # Add SANDBOX_SECRET to environment variables
        if env is None:
            env = {}
        env["SANDBOX_SECRET"] = sandbox_secret

        # Check if light sleep is enabled for this instance type
        light_sleep_enabled = _is_light_sleep_enabled(
            instance_type, catalog_instances_api
        )

        app_name = f"sandbox-app-{name}-{int(time.time())}"
        app_response = apps_api.create_app(app=CreateApp(name=app_name))
        app_id = app_response.app.id

        env_vars = build_env_vars(env)
        docker_source = create_docker_source(image, [])
        deployment_definition = create_deployment_definition(
            name=f"sandbox-service-{name}",
            docker_source=docker_source,
            env_vars=env_vars,
            instance_type=instance_type,
            exposed_port_protocol=exposed_port_protocol,
            regions=regions,
            routes=routes,
            idle_timeout=idle_timeout,
            light_sleep_enabled=light_sleep_enabled,
            enable_tcp_proxy=enable_tcp_proxy,
        )

        create_service = CreateService(app_id=app_id, definition=deployment_definition)
        service_response = services_api.create_service(service=create_service)
        service_id = service_response.service.id
        deployment_id = service_response.service.latest_deployment_id

        deployments_api = DeploymentsApi(services_api.api_client)

        max_wait = min(timeout // 2, 60) if timeout > 60 else timeout
        wait_interval = 0.5
        start_time = time.time()

        while time.time() - start_time < max_wait:
            try:
                scaling_response = deployments_api.get_deployment_scaling(
                    id=deployment_id
                )

                if scaling_response.replicas and scaling_response.replicas[0].instances:
                    instance_id = scaling_response.replicas[0].instances[0].id
                    break
                else:
                    logger.debug(
                        f"Waiting for instances to be created... (elapsed: {time.time() - start_time:.1f}s)"
                    )
                    time.sleep(wait_interval)
            except Exception as e:
                logger.warning(f"Error getting deployment scaling: {e}")
                time.sleep(wait_interval)
        else:
            raise SandboxError(
                f"No instances found in deployment after {max_wait} seconds"
            )

        return cls(
            sandbox_id=name,
            app_id=app_id,
            service_id=service_id,
            instance_id=instance_id,
            name=name,
            api_token=api_token,
            sandbox_secret=sandbox_secret,
        )

    def wait_ready(
        self,
        timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> bool:
        """
        Wait for sandbox to become ready with proper polling.

        Args:
            timeout: Maximum time to wait in seconds
            poll_interval: Time between health checks in seconds

        Returns:
            bool: True if sandbox became ready, False if timeout
        """
        start_time = time.time()
        sandbox_url = None

        while time.time() - start_time < timeout:
            # Get sandbox URL on first iteration or if not yet retrieved
            if sandbox_url is None:
                sandbox_url = self._get_sandbox_url()
                # If URL is not available yet, wait and retry
                if sandbox_url is None:
                    time.sleep(poll_interval)
                    continue

            is_healthy = is_sandbox_healthy(
                self.instance_id,
                sandbox_url=sandbox_url,
                sandbox_secret=self.sandbox_secret,
                api_token=self.api_token,
            )

            if is_healthy:
                return True

            time.sleep(poll_interval)

        return False

    def wait_tcp_proxy_ready(
        self,
        timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> bool:
        """
        Wait for TCP proxy to become ready and available.

        Polls the deployment metadata until the TCP proxy information is available.
        This is useful when enable_tcp_proxy=True was set during sandbox creation,
        as the proxy information may not be immediately available.

        Args:
            timeout: Maximum time to wait in seconds
            poll_interval: Time between checks in seconds

        Returns:
            bool: True if TCP proxy became ready, False if timeout
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            tcp_proxy_info = self.get_tcp_proxy_info()
            if tcp_proxy_info is not None:
                return True

            time.sleep(poll_interval)

        return False

    def delete(self) -> None:
        """Delete the sandbox instance."""
        apps_api, services_api, _, _ = get_api_client(self.api_token)
        services_api.delete_service(self.service_id)
        apps_api.delete_app(self.app_id)

    def get_domain(self) -> Optional[str]:
        """
        Get the public domain of the sandbox.

        Returns the domain name (e.g., "app-name-org.koyeb.app") without protocol or path.
        To construct the URL, use: f"https://{sandbox.get_domain()}"

        Returns:
            Optional[str]: The domain name or None if unavailable
        """
        try:
            from koyeb.api.exceptions import ApiException, NotFoundException

            from .utils import get_api_client

            _, services_api, _, _ = get_api_client(self.api_token)
            service_response = services_api.get_service(self.service_id)
            service = service_response.service

            if service.app_id:
                apps_api, _, _, _ = get_api_client(self.api_token)
                app_response = apps_api.get_app(service.app_id)
                app = app_response.app
                if hasattr(app, "domains") and app.domains:
                    # Use the first public domain
                    return app.domains[0].name
            return None
        except (NotFoundException, ApiException, Exception):
            return None

    def get_tcp_proxy_info(self) -> Optional[tuple[str, int]]:
        """
        Get the TCP proxy host and port for the sandbox.

        Returns the TCP proxy host and port as a tuple (host, port) for direct TCP access to port 3031.
        This is only available if enable_tcp_proxy=True was set when creating the sandbox.

        Returns:
            Optional[tuple[str, int]]: A tuple of (host, port) or None if unavailable
        """
        try:
            from koyeb.api.exceptions import ApiException, NotFoundException

            from .utils import get_api_client

            _, services_api, _, _ = get_api_client(self.api_token)
            service_response = services_api.get_service(self.service_id)
            service = service_response.service

            if not service.active_deployment_id:
                return None

            # Get the active deployment
            deployments_api = DeploymentsApi()
            deployments_api.api_client = services_api.api_client
            deployment_response = deployments_api.get_deployment(
                service.active_deployment_id
            )
            deployment = deployment_response.deployment

            if not deployment.metadata or not deployment.metadata.proxy_ports:
                return None

            # Find the proxy port for port 3031
            for proxy_port in deployment.metadata.proxy_ports:
                if (
                    proxy_port.port == 3031
                    and proxy_port.host
                    and proxy_port.public_port
                ):
                    return (proxy_port.host, proxy_port.public_port)

            return None
        except (NotFoundException, ApiException, Exception):
            return None

    def _get_sandbox_url(self) -> Optional[str]:
        """
        Internal method to get the sandbox URL for health checks and client initialization.
        Caches the URL after first retrieval.

        Returns:
            Optional[str]: The sandbox URL or None if unavailable
        """
        if self._sandbox_url is None:
            domain = self.get_domain()
            if domain:
                self._sandbox_url = f"https://{domain}/koyeb-sandbox"
        return self._sandbox_url

    def _get_client(self) -> "SandboxClient":  # type: ignore[name-defined]
        """
        Get or create SandboxClient instance with validation.

        Returns:
            SandboxClient: Configured client instance

        Raises:
            SandboxError: If sandbox URL or secret is not available
        """
        if self._client is None:
            sandbox_url = self._get_sandbox_url()
            self._client = create_sandbox_client(sandbox_url, self.sandbox_secret)
        return self._client

    def _check_response_error(self, response: Dict, operation: str) -> None:
        """
        Check if a response indicates an error and raise SandboxError if so.

        Args:
            response: The response dictionary to check
            operation: Description of the operation (e.g., "expose port 8080")

        Raises:
            SandboxError: If response indicates failure
        """
        if not response.get("success", False):
            error_msg = response.get("error", "Unknown error")
            raise SandboxError(f"Failed to {operation}: {error_msg}")

    def status(self) -> str:
        """Get current sandbox status"""
        from .utils import get_sandbox_status

        status = get_sandbox_status(self.instance_id, self.api_token)
        return status.value

    def is_healthy(self) -> bool:
        """Check if sandbox is healthy and ready for operations"""
        sandbox_url = self._get_sandbox_url()
        return is_sandbox_healthy(
            self.instance_id,
            sandbox_url=sandbox_url,
            sandbox_secret=self.sandbox_secret,
            api_token=self.api_token,
        )

    @property
    def filesystem(self) -> "SandboxFilesystem":
        """Get filesystem operations interface"""
        from .filesystem import SandboxFilesystem

        return SandboxFilesystem(self)

    @property
    def exec(self) -> "SandboxExecutor":
        """Get command execution interface"""
        from .exec import SandboxExecutor

        return SandboxExecutor(self)

    def expose_port(self, port: int) -> ExposedPort:
        """
        Expose a port to external connections via TCP proxy.

        Binds the specified internal port to the TCP proxy, allowing external
        connections to reach services running on that port inside the sandbox.
        Automatically unbinds any existing port before binding the new one.

        Args:
            port: The internal port number to expose (must be a valid port number between 1 and 65535)

        Returns:
            ExposedPort: An object with `port` and `exposed_at` attributes:
                - port: The exposed port number
                - exposed_at: The full URL with https:// protocol (e.g., "https://app-name-org.koyeb.app")

        Raises:
            ValueError: If port is not in valid range [1, 65535]
            SandboxError: If the port binding operation fails

        Notes:
            - Only one port can be exposed at a time
            - Any existing port binding is automatically unbound before binding the new port
            - The port must be available and accessible within the sandbox environment
            - The TCP proxy is accessed via get_tcp_proxy_info() which returns (host, port)

        Example:
            >>> result = sandbox.expose_port(8080)
            >>> result.port
            8080
            >>> result.exposed_at
            'https://app-name-org.koyeb.app'
        """
        validate_port(port)
        client = self._get_client()
        try:
            # Always unbind any existing port first
            try:
                client.unbind_port()
            except Exception as e:
                # Ignore errors when unbinding - it's okay if no port was bound
                logger.debug(f"Error unbinding existing port (this is okay): {e}")
                pass

            # Now bind the new port
            response = client.bind_port(port)
            self._check_response_error(response, f"expose port {port}")

            # Get domain for exposed_at
            domain = self.get_domain()
            if not domain:
                raise SandboxError("Domain not available for exposed port")

            # Return the port from response if available, otherwise use the requested port
            exposed_port = int(response.get("port", port))
            exposed_at = f"https://{domain}"
            return ExposedPort(port=exposed_port, exposed_at=exposed_at)
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to expose port {port}: {str(e)}") from e

    def unexpose_port(self) -> None:
        """
        Unexpose a port from external connections.

        Removes the TCP proxy port binding, stopping traffic forwarding to the
        previously bound port.

        Raises:
            SandboxError: If the port unbinding operation fails

        Notes:
            - After unexposing, the TCP proxy will no longer forward traffic
            - Safe to call even if no port is currently bound
        """
        client = self._get_client()
        try:
            response = client.unbind_port()
            self._check_response_error(response, "unexpose port")
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to unexpose port: {str(e)}") from e

    def launch_process(
        self, cmd: str, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Launch a background process in the sandbox.

        Starts a long-running background process that continues executing even after
        the method returns. Use this for servers, workers, or other long-running tasks.

        Args:
            cmd: The shell command to execute as a background process
            cwd: Optional working directory for the process
            env: Optional environment variables to set/override for the process

        Returns:
            str: The unique process ID (UUID string) that can be used to manage the process

        Raises:
            SandboxError: If the process launch fails

        Example:
            >>> process_id = sandbox.launch_process("python -u server.py")
            >>> print(f"Started process: {process_id}")
        """
        client = self._get_client()
        try:
            response = client.start_process(cmd, cwd, env)
            # Check for process ID - if it exists, the process was launched successfully
            process_id = response.get("id")
            if process_id:
                return process_id
            # If no ID, check for explicit error
            error_msg = response.get("error", response.get("message", "Unknown error"))
            raise SandboxError(f"Failed to launch process: {error_msg}")
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to launch process: {str(e)}") from e

    def kill_process(self, process_id: str) -> None:
        """
        Kill a background process by its ID.

        Terminates a running background process. This sends a SIGTERM signal to the process,
        allowing it to clean up gracefully. If the process doesn't terminate within a timeout,
        it will be forcefully killed with SIGKILL.

        Args:
            process_id: The unique process ID (UUID string) to kill

        Raises:
            SandboxError: If the process kill operation fails

        Example:
            >>> sandbox.kill_process("550e8400-e29b-41d4-a716-446655440000")
        """
        client = self._get_client()
        try:
            response = client.kill_process(process_id)
            self._check_response_error(response, f"kill process {process_id}")
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to kill process {process_id}: {str(e)}") from e

    def list_processes(self) -> List[ProcessInfo]:
        """
        List all background processes.

        Returns information about all currently running and recently completed background
        processes. This includes both active processes and processes that have completed
        (which remain in memory until server restart).

        Returns:
            List[ProcessInfo]: List of process dictionaries, each containing:
                - id: Process ID (UUID string)
                - cmd: The command that was executed
                - status: Process status (e.g., "running", "completed")
                - pid: OS process ID (if running)
                - exit_code: Exit code (if completed)
                - started_at: ISO 8601 timestamp when process started
                - completed_at: ISO 8601 timestamp when process completed (if applicable)

        Raises:
            SandboxError: If listing processes fails

        Example:
            >>> processes = sandbox.list_processes()
            >>> for process in processes:
            ...     print(f"{process['id']}: {process['cmd']} - {process['status']}")
        """
        client = self._get_client()
        try:
            response = client.list_processes()
            return response.get("processes", [])
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to list processes: {str(e)}") from e

    def kill_all_processes(self) -> int:
        """
        Kill all running background processes.

        Convenience method that lists all processes and kills them all. This is useful
        for cleanup operations.

        Returns:
            int: The number of processes that were killed

        Raises:
            SandboxError: If listing or killing processes fails

        Example:
            >>> count = sandbox.kill_all_processes()
            >>> print(f"Killed {count} processes")
        """
        processes = self.list_processes()
        killed_count = 0
        for process in processes:
            process_id = process.get("id")
            status = process.get("status", "")
            # Only kill running processes
            if process_id and status == "running":
                try:
                    self.kill_process(process_id)
                    killed_count += 1
                except SandboxError:
                    # Continue killing other processes even if one fails
                    pass
        return killed_count

    def __enter__(self) -> "Sandbox":
        """Context manager entry - returns self."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - automatically deletes the sandbox."""
        try:
            # Clean up client if it exists
            if self._client is not None:
                self._client.close()
            self.delete()
        except Exception as e:
            logger.warning(f"Error during sandbox cleanup: {e}")


class AsyncSandbox(Sandbox):
    """
    Async sandbox for running code on Koyeb infrastructure.
    Inherits from Sandbox and provides async wrappers for all operations.
    """

    def _run_sync(self, method, *args, **kwargs):
        """
        Helper method to run a synchronous method in an executor.

        Args:
            method: The sync method to run (from super())
            *args: Positional arguments for the method
            **kwargs: Keyword arguments for the method

        Returns:
            Result of the synchronous method call
        """
        return run_sync_in_executor(method, *args, **kwargs)

    @classmethod
    async def create(
        cls,
        image: str = "koyeb/sandbox",
        name: str = "quick-sandbox",
        wait_ready: bool = True,
        instance_type: str = "nano",
        exposed_port_protocol: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        regions: Optional[List[str]] = None,
        api_token: Optional[str] = None,
        timeout: int = 300,
        idle_timeout: Optional[IdleTimeout] = None,
        enable_tcp_proxy: bool = False,
    ) -> AsyncSandbox:
        """
            Create a new sandbox instance with async support.

            Args:
                image: Docker image to use (default: koyeb/sandbox)
                name: Name of the sandbox
                wait_ready: Wait for sandbox to be ready (default: True)
                instance_type: Instance type (default: nano)
                exposed_port_protocol: Protocol to expose ports with ("http" or "http2").
                    If None, defaults to "http".
                    If provided, must be one of "http" or "http2".
                env: Environment variables
                regions: List of regions to deploy to (default: ["na"])
                api_token: Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
                timeout: Timeout for sandbox creation in seconds
                idle_timeout: Idle timeout configuration for scale-to-zero
                    - None: Auto-enable (light_sleep=300s, deep_sleep=600s)
                    - 0: Disable scale-to-zero (keep always-on)
                    - int > 0: Deep sleep only (e.g., 600 for 600s deep sleep)
                    - dict: Explicit configuration with {"light_sleep": 300, "deep_sleep": 600}
                enable_tcp_proxy: If True, enables TCP proxy for direct TCP access to port 3031

        Returns:
                AsyncSandbox: A new AsyncSandbox instance
        """
        if api_token is None:
            api_token = os.getenv("KOYEB_API_TOKEN")
            if not api_token:
                raise ValueError(
                    "API token is required. Set KOYEB_API_TOKEN environment variable or pass api_token parameter"
                )

        loop = asyncio.get_running_loop()
        sync_result = await loop.run_in_executor(
            None,
            lambda: Sandbox._create_sync(
                name=name,
                image=image,
                instance_type=instance_type,
                exposed_port_protocol=exposed_port_protocol,
                env=env,
                regions=regions,
                api_token=api_token,
                timeout=timeout,
                idle_timeout=idle_timeout,
                enable_tcp_proxy=enable_tcp_proxy,
            ),
        )

        # Convert Sandbox instance to AsyncSandbox instance
        sandbox = cls(
            sandbox_id=sync_result.sandbox_id,
            app_id=sync_result.app_id,
            service_id=sync_result.service_id,
            instance_id=sync_result.instance_id,
            name=sync_result.name,
            api_token=sync_result.api_token,
            sandbox_secret=sync_result.sandbox_secret,
        )
        sandbox._created_at = sync_result._created_at

        if wait_ready:
            await sandbox.wait_ready(timeout=timeout)

        return sandbox

    async def wait_ready(
        self,
        timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> bool:
        """
        Wait for sandbox to become ready with proper async polling.

        Args:
            timeout: Maximum time to wait in seconds
            poll_interval: Time between health checks in seconds

        Returns:
            bool: True if sandbox became ready, False if timeout
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            loop = asyncio.get_running_loop()
            is_healthy = await loop.run_in_executor(None, super().is_healthy)

            if is_healthy:
                return True

            await asyncio.sleep(poll_interval)

        return False

    async def wait_tcp_proxy_ready(
        self,
        timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> bool:
        """
        Wait for TCP proxy to become ready and available asynchronously.

        Polls the deployment metadata until the TCP proxy information is available.
        This is useful when enable_tcp_proxy=True was set during sandbox creation,
        as the proxy information may not be immediately available.

        Args:
            timeout: Maximum time to wait in seconds
            poll_interval: Time between checks in seconds

        Returns:
            bool: True if TCP proxy became ready, False if timeout
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            loop = asyncio.get_running_loop()
            tcp_proxy_info = await loop.run_in_executor(
                None, super().get_tcp_proxy_info
            )
            if tcp_proxy_info is not None:
                return True

            await asyncio.sleep(poll_interval)

        return False

    async def delete(self) -> None:
        """Delete the sandbox instance asynchronously."""
        await self._run_sync(super().delete)

    async def status(self) -> str:
        """Get current sandbox status asynchronously"""
        return await self._run_sync(super().status)

    async def is_healthy(self) -> bool:
        """Check if sandbox is healthy and ready for operations asynchronously"""
        return await self._run_sync(super().is_healthy)

    @property
    def exec(self) -> "AsyncSandboxExecutor":
        """Get async command execution interface"""
        from .exec import AsyncSandboxExecutor

        return AsyncSandboxExecutor(self)

    @property
    def filesystem(self) -> "AsyncSandboxFilesystem":
        """Get filesystem operations interface"""
        from .filesystem import AsyncSandboxFilesystem

        return AsyncSandboxFilesystem(self)

    async def expose_port(self, port: int) -> ExposedPort:
        """Expose a port to external connections via TCP proxy asynchronously."""
        return await self._run_sync(super().expose_port, port)

    async def unexpose_port(self) -> None:
        """Unexpose a port from external connections asynchronously."""
        await self._run_sync(super().unexpose_port)

    async def launch_process(
        self, cmd: str, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None
    ) -> str:
        """Launch a background process in the sandbox asynchronously."""
        return await self._run_sync(super().launch_process, cmd, cwd, env)

    async def kill_process(self, process_id: str) -> None:
        """Kill a background process by its ID asynchronously."""
        await self._run_sync(super().kill_process, process_id)

    async def list_processes(self) -> List[ProcessInfo]:
        """List all background processes asynchronously."""
        return await self._run_sync(super().list_processes)

    async def kill_all_processes(self) -> int:
        """Kill all running background processes asynchronously."""
        return await self._run_sync(super().kill_all_processes)

    async def __aenter__(self) -> "AsyncSandbox":
        """Async context manager entry - returns self."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit - automatically deletes the sandbox."""
        try:
            # Clean up client if it exists
            if self._client is not None:
                self._client.close()
            await self.delete()
        except Exception as e:
            logger.warning(f"Error during sandbox cleanup: {e}")
