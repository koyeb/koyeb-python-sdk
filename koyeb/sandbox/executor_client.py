"""
Sandbox Executor API Client

A simple Python client for interacting with the Sandbox Executor API.
"""

import time
from typing import Any, Dict, Iterator, Optional

import requests


class SandboxClient:
    """Client for the Sandbox Executor API."""

    def __init__(self, base_url: str, secret: str):
        """
        Initialize the Sandbox Client.

        Args:
            base_url: The base URL of the sandbox server (e.g., 'http://localhost:8080')
            secret: The authentication secret/token
        """
        self.base_url = base_url.rstrip("/")
        self.secret = secret
        self.headers = {
            "Authorization": f"Bearer {secret}",
            "Content-Type": "application/json",
        }

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

        for attempt in range(max_retries + 1):
            try:
                response = requests.request(method, url, **kwargs)

                # If we get a 503, retry with backoff
                if response.status_code == 503 and attempt < max_retries:
                    time.sleep(backoff)
                    backoff *= 2  # Exponential backoff
                    continue

                response.raise_for_status()
                return response

            except requests.HTTPError as e:
                if e.response.status_code == 503 and attempt < max_retries:
                    time.sleep(backoff)
                    backoff *= 2
                    last_exception = e
                    continue
                raise

        # If we exhausted all retries, raise the last exception
        if last_exception:
            raise last_exception

    def health(self) -> Dict[str, str]:
        """
        Check the health status of the server.

        Returns:
            Dict with status information
        """
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        if response.status_code != 200:
            return {"status": "unhealthy"}
        return response.json()

    def run(
        self, cmd: str, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Execute a shell command in the sandbox.

        Args:
            cmd: The shell command to execute
            cwd: Optional working directory for command execution
            env: Optional environment variables to set/override

        Returns:
            Dict containing stdout, stderr, error (if any), and exit code
        """
        payload = {"cmd": cmd}
        if cwd is not None:
            payload["cwd"] = cwd
        if env is not None:
            payload["env"] = env

        response = self._request_with_retry(
            "POST", f"{self.base_url}/run", json=payload, headers=self.headers
        )
        return response.json()

    def run_streaming(
        self, cmd: str, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None
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
        import json

        payload = {"cmd": cmd}
        if cwd is not None:
            payload["cwd"] = cwd
        if env is not None:
            payload["env"] = env

        response = requests.post(
            f"{self.base_url}/run_streaming",
            json=payload,
            headers=self.headers,
            stream=True,
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
