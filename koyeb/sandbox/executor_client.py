"""
Sandbox Executor API Client

A simple Python client for interacting with the Sandbox Executor API.
"""

import json
import logging
import time
from typing import Any, Dict, Iterator, Optional

import requests

from .utils import DEFAULT_HTTP_TIMEOUT

logger = logging.getLogger(__name__)


class SandboxClient:
    """Client for the Sandbox Executor API."""

    def __init__(
        self, base_url: str, secret: str, timeout: float = DEFAULT_HTTP_TIMEOUT
    ):
        """
        Initialize the Sandbox Client.

        Args:
            base_url: The base URL of the sandbox server (e.g., 'http://localhost:8080')
            secret: The authentication secret/token
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url.rstrip("/")
        self.secret = secret
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {secret}",
            "Content-Type": "application/json",
        }
        # Use session for connection pooling
        self._session = requests.Session()
        self._session.headers.update(self.headers)
        self._closed = False

    def close(self) -> None:
        """Close the HTTP session and release resources."""
        if not self._closed and hasattr(self, "_session"):
            self._session.close()
            self._closed = True

    def __enter__(self):
        """Context manager entry - returns self."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - automatically closes the session."""
        self.close()

    def __del__(self):
        """Clean up session on deletion (fallback, not guaranteed to run)."""
        if not self._closed:
            self.close()

    def _request_with_retry(
        self,
        method: str,
        url: str,
        max_retries: int = 3,
        initial_backoff: float = 1.0,
        **kwargs,
    ) -> requests.Response:
        """
        Make an HTTP request with retry logic for 503 errors.

        Args:
            method: HTTP method (e.g., 'GET', 'POST')
            url: The URL to request
            max_retries: Maximum number of retry attempts
            initial_backoff: Initial backoff time in seconds (doubles each retry)
            **kwargs: Additional arguments to pass to requests

        Returns:
            Response object

        Raises:
            requests.HTTPError: If the request fails after all retries
        """
        backoff = initial_backoff
        last_exception = None

        # Set default timeout if not provided
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        for attempt in range(max_retries + 1):
            try:
                # Use session for connection pooling
                response = self._session.request(method, url, **kwargs)

                # If we get a 503, retry with backoff
                if response.status_code == 503 and attempt < max_retries:
                    logger.debug(
                        f"Received 503 error, retrying... (attempt {attempt + 1}/{max_retries + 1})"
                    )
                    time.sleep(backoff)
                    backoff *= 2  # Exponential backoff
                    continue

                response.raise_for_status()
                return response

            except requests.HTTPError as e:
                if (
                    e.response
                    and e.response.status_code == 503
                    and attempt < max_retries
                ):
                    logger.debug(
                        f"Received 503 error, retrying... (attempt {attempt + 1}/{max_retries + 1})"
                    )
                    time.sleep(backoff)
                    backoff *= 2
                    last_exception = e
                    continue
                raise
            except requests.Timeout as e:
                logger.warning(f"Request timeout after {self.timeout}s: {e}")
                raise
            except requests.RequestException as e:
                logger.warning(f"Request failed: {e}")
                raise

        # If we exhausted all retries, raise the last exception
        if last_exception:
            raise last_exception

    def health(self) -> Dict[str, str]:
        """
        Check the health status of the server.

        Returns:
            Dict with status information

        Raises:
            requests.HTTPError: If the health check fails
        """
        response = self._request_with_retry(
            "GET", f"{self.base_url}/health", timeout=self.timeout
        )
        return response.json()

    def run(
        self,
        cmd: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Execute a shell command in the sandbox.

        Args:
            cmd: The shell command to execute
            cwd: Optional working directory for command execution
            env: Optional environment variables to set/override
            timeout: Optional timeout in seconds for the request

        Returns:
            Dict containing stdout, stderr, error (if any), and exit code
        """
        payload = {"cmd": cmd}
        if cwd is not None:
            payload["cwd"] = cwd
        if env is not None:
            payload["env"] = env

        request_timeout = timeout if timeout is not None else self.timeout
        response = self._request_with_retry(
            "POST",
            f"{self.base_url}/run",
            json=payload,
            headers=self.headers,
            timeout=request_timeout,
        )
        return response.json()

    def run_streaming(
        self,
        cmd: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[Dict[str, Any]]:
        """
        Execute a shell command in the sandbox and stream the output in real-time.

        This method uses Server-Sent Events (SSE) to stream command output line-by-line
        as it's produced. Use this for long-running commands where you want real-time
        output. For simple commands where buffered output is acceptable, use run() instead.

        Args:
            cmd: The shell command to execute
            cwd: Optional working directory for command execution
            env: Optional environment variables to set/override
            timeout: Optional timeout in seconds for the streaming request

        Yields:
            Dict events with the following types:

            - output events (as command produces output):
              {"stream": "stdout"|"stderr", "data": "line of output"}

            - complete event (when command finishes):
              {"code": <exit_code>, "error": false}

            - error event (if command fails to start):
              {"error": "error message"}

        Example:
            >>> client = SandboxClient("http://localhost:8080", "secret")
            >>> for event in client.run_streaming("echo 'Hello'; sleep 1; echo 'World'"):
            ...     if "stream" in event:
            ...         print(f"{event['stream']}: {event['data']}")
            ...     elif "code" in event:
            ...         print(f"Exit code: {event['code']}")
        """
        payload = {"cmd": cmd}
        if cwd is not None:
            payload["cwd"] = cwd
        if env is not None:
            payload["env"] = env

        response = self._session.post(
            f"{self.base_url}/run_streaming",
            json=payload,
            headers=self.headers,
            stream=True,
            timeout=timeout if timeout is not None else self.timeout,
        )
        response.raise_for_status()

        # Parse Server-Sent Events stream
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            if line.startswith("data:"):
                data = line[5:].strip()
                try:
                    event_data = json.loads(data)
                    yield event_data
                except json.JSONDecodeError:
                    # If we can't parse the JSON, yield the raw data
                    yield {"error": f"Failed to parse event data: {data}"}

    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """
        Write content to a file.

        Args:
            path: The file path to write to
            content: The content to write

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path, "content": content}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/write_file", json=payload, headers=self.headers
        )
        return response.json()

    def read_file(self, path: str) -> Dict[str, Any]:
        """
        Read content from a file.

        Args:
            path: The file path to read from

        Returns:
            Dict with file content and error if any
        """
        payload = {"path": path}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/read_file", json=payload, headers=self.headers
        )
        return response.json()

    def delete_file(self, path: str) -> Dict[str, Any]:
        """
        Delete a file.

        Args:
            path: The file path to delete

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/delete_file", json=payload, headers=self.headers
        )
        return response.json()

    def make_dir(self, path: str) -> Dict[str, Any]:
        """
        Create a directory (including parent directories).

        Args:
            path: The directory path to create

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/make_dir", json=payload, headers=self.headers
        )
        return response.json()

    def delete_dir(self, path: str) -> Dict[str, Any]:
        """
        Recursively delete a directory and all its contents.

        Args:
            path: The directory path to delete

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/delete_dir", json=payload, headers=self.headers
        )
        return response.json()

    def list_dir(self, path: str) -> Dict[str, Any]:
        """
        List the contents of a directory.

        Args:
            path: The directory path to list

        Returns:
            Dict with entries list and error if any
        """
        payload = {"path": path}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/list_dir", json=payload, headers=self.headers
        )
        return response.json()

    def bind_port(self, port: int) -> Dict[str, Any]:
        """
        Bind a port to the TCP proxy for external access.

        Configures the TCP proxy to forward traffic to the specified port inside the sandbox.
        This allows you to expose services running inside the sandbox to external connections.

        Args:
            port: The port number to bind to (must be a valid port number)

        Returns:
            Dict with success status, message, and port information

        Notes:
            - Only one port can be bound at a time
            - Binding a new port will override the previous binding
            - The port must be available and accessible within the sandbox environment
        """
        payload = {"port": str(port)}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/bind_port", json=payload, headers=self.headers
        )
        return response.json()

    def unbind_port(self, port: Optional[int] = None) -> Dict[str, Any]:
        """
        Unbind a port from the TCP proxy.

        Removes the TCP proxy port binding, stopping traffic forwarding to the previously bound port.

        Args:
            port: Optional port number to unbind. If provided, it must match the currently bound port.
                If not provided, any existing binding will be removed.

        Returns:
            Dict with success status and message

        Notes:
            - If a port is specified and doesn't match the currently bound port, the request will fail
            - After unbinding, the TCP proxy will no longer forward traffic
        """
        payload = {}
        if port is not None:
            payload["port"] = str(port)
        response = self._request_with_retry(
            "POST", f"{self.base_url}/unbind_port", json=payload, headers=self.headers
        )
        return response.json()

    def start_process(
        self, cmd: str, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Start a background process in the sandbox.

        Starts a long-running background process that continues executing even after
        the API call completes. Use this for servers, workers, or other long-running tasks.

        Args:
            cmd: The shell command to execute as a background process
            cwd: Optional working directory for the process
            env: Optional environment variables to set/override for the process

        Returns:
            Dict with process id and success status:
                - id: The unique process ID (UUID string)
                - success: True if the process was started successfully

        Example:
            >>> client = SandboxClient("http://localhost:8080", "secret")
            >>> result = client.start_process("python -u server.py")
            >>> process_id = result["id"]
            >>> print(f"Started process: {process_id}")
        """
        payload = {"cmd": cmd}
        if cwd is not None:
            payload["cwd"] = cwd
        if env is not None:
            payload["env"] = env

        response = self._request_with_retry(
            "POST", f"{self.base_url}/start_process", json=payload, headers=self.headers
        )
        return response.json()

    def kill_process(self, process_id: str) -> Dict[str, Any]:
        """
        Kill a background process by its ID.

        Terminates a running background process. This sends a SIGTERM signal to the process,
        allowing it to clean up gracefully. If the process doesn't terminate within a timeout,
        it will be forcefully killed with SIGKILL.

        Args:
            process_id: The unique process ID (UUID string) to kill

        Returns:
            Dict with success status and error message if any

        Example:
            >>> client = SandboxClient("http://localhost:8080", "secret")
            >>> result = client.kill_process("550e8400-e29b-41d4-a716-446655440000")
            >>> if result.get("success"):
            ...     print("Process killed successfully")
        """
        payload = {"id": process_id}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/kill_process", json=payload, headers=self.headers
        )
        return response.json()

    def list_processes(self) -> Dict[str, Any]:
        """
        List all background processes.

        Returns information about all currently running and recently completed background
        processes. This includes both active processes and processes that have completed
        (which remain in memory until server restart).

        Returns:
            Dict with a list of processes:
                - processes: List of process objects, each containing:
                    - id: Process ID (UUID string)
                    - command: The command that was executed
                    - status: Process status (e.g., "running", "completed")
                    - pid: OS process ID (if running)
                    - exit_code: Exit code (if completed)
                    - started_at: ISO 8601 timestamp when process started
                    - completed_at: ISO 8601 timestamp when process completed (if applicable)

        Example:
            >>> client = SandboxClient("http://localhost:8080", "secret")
            >>> result = client.list_processes()
            >>> for process in result.get("processes", []):
            ...     print(f"{process['id']}: {process['command']} - {process['status']}")
        """
        response = self._request_with_retry(
            "GET", f"{self.base_url}/list_processes", headers=self.headers
        )
        return response.json()
