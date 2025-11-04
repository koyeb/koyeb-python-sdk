# coding: utf-8

"""
Koyeb Sandbox - Python SDK for creating and managing Koyeb sandboxes
"""

from __future__ import annotations

import asyncio
import os
import secrets
import time
from typing import TYPE_CHECKING, Dict, List, Optional

from koyeb.api.models.create_app import CreateApp

from .utils import (
    IdleTimeout,
    build_env_vars,
    create_deployment_definition,
    create_docker_source,
    create_koyeb_sandbox_routes,
    get_api_client,
    is_sandbox_healthy,
)

if TYPE_CHECKING:
    from .exec import AsyncSandboxExecutor, SandboxExecutor
    from .filesystem import AsyncSandboxFilesystem, SandboxFilesystem


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
        from .utils import _is_light_sleep_enabled

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
        )

        from koyeb.api.models.create_service import CreateService

        create_service = CreateService(app_id=app_id, definition=deployment_definition)
        service_response = services_api.create_service(service=create_service)
        service_id = service_response.service.id
        deployment_id = service_response.service.latest_deployment_id

        from koyeb.api.api.deployments_api import DeploymentsApi

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
                    print(
                        f"Waiting for instances to be created... (elapsed: {time.time() - start_time:.1f}s)"
                    )
                    time.sleep(wait_interval)
            except Exception as e:
                print(f"Error getting deployment scaling: {e}")
                time.sleep(wait_interval)
        else:
            raise Exception(
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

    def wait_ready(self, timeout: int = 60, poll_interval: float = 2.0) -> bool:
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
                sandbox_url = self.get_sandbox_url()
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

    def delete(self) -> None:
        """Delete the sandbox instance."""
        apps_api, services_api, _, _ = get_api_client(self.api_token)
        services_api.delete_service(self.service_id)
        apps_api.delete_app(self.app_id)

    def get_sandbox_url(self) -> Optional[str]:
        """
        Get the public URL of the sandbox.
        Caches the URL after first retrieval.

        Returns:
            Optional[str]: The sandbox URL or None if unavailable
        """
        if self._sandbox_url is None:
            from .utils import get_sandbox_url

            self._sandbox_url = get_sandbox_url(self.service_id, self.api_token)
        return self._sandbox_url

    def status(self) -> str:
        """Get current sandbox status"""
        from .utils import get_sandbox_status

        status = get_sandbox_status(self.instance_id, self.api_token)
        return status.value

    def is_healthy(self) -> bool:
        """Check if sandbox is healthy and ready for operations"""
        sandbox_url = self.get_sandbox_url()
        return is_sandbox_healthy(
            self.instance_id,
            sandbox_url=sandbox_url,
            sandbox_secret=self.sandbox_secret,
            api_token=self.api_token,
        )

    @property
    def filesystem(self) -> SandboxFilesystem:
        """Get filesystem operations interface"""
        from .filesystem import SandboxFilesystem

        return SandboxFilesystem(self)

    @property
    def exec(self) -> SandboxExecutor:
        """Get command execution interface"""
        from .exec import SandboxExecutor

        return SandboxExecutor(self)


class AsyncSandbox(Sandbox):
    """
    Async sandbox for running code on Koyeb infrastructure.
    Inherits from Sandbox and provides async wrappers for all operations.
    """

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

    async def wait_ready(self, timeout: int = 60, poll_interval: float = 2.0) -> bool:
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

    async def delete(self) -> None:
        """Delete the sandbox instance asynchronously."""
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, super().delete)

    async def status(self) -> str:
        """Get current sandbox status asynchronously"""
        loop = asyncio.get_running_loop()
        status_value = await loop.run_in_executor(None, super().status)
        return status_value

    async def is_healthy(self) -> bool:
        """Check if sandbox is healthy and ready for operations asynchronously"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, super().is_healthy)

    @property
    def exec(self) -> AsyncSandboxExecutor:
        """Get async command execution interface"""
        from .exec import AsyncSandboxExecutor

        return AsyncSandboxExecutor(self)

    @property
    def filesystem(self) -> AsyncSandboxFilesystem:
        """Get filesystem operations interface"""
        from .filesystem import AsyncSandboxFilesystem

        return AsyncSandboxFilesystem(self)
