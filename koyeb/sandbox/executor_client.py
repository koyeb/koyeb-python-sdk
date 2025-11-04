"""
Sandbox Executor API Client

A simple Python client for interacting with the Sandbox Executor API.
"""

import requests
from typing import Optional, Dict, List, Any


class SandboxClient:
    """Client for the Sandbox Executor API."""
    
    def __init__(self, base_url: str, secret: str):
        """
        Initialize the Sandbox Client.
        
        Args:
            base_url: The base URL of the sandbox server (e.g., 'http://localhost:8080')
            secret: The authentication secret/token
        """
        self.base_url = base_url.rstrip('/')
        self.secret = secret
        self.headers = {
            'Authorization': f'Bearer {secret}',
            'Content-Type': 'application/json'
        }
    
    def health(self) -> Dict[str, str]:
        """
        Check the health status of the server.
        
        Returns:
            Dict with status information
        """
        response = requests.get(f'{self.base_url}/health')
        response.raise_for_status()
        return response.json()
    
    def run(
        self,
        cmd: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None
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
        payload = {'cmd': cmd}
        if cwd is not None:
            payload['cwd'] = cwd
        if env is not None:
            payload['env'] = env
        
        response = requests.post(
            f'{self.base_url}/run',
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """
        Write content to a file.
        
        Args:
            path: The file path to write to
            content: The content to write
            
        Returns:
            Dict with success status and error if any
        """
        payload = {
            'path': path,
            'content': content
        }
        response = requests.post(
            f'{self.base_url}/write_file',
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def read_file(self, path: str) -> Dict[str, Any]:
        """
        Read content from a file.
        
        Args:
            path: The file path to read from
            
        Returns:
            Dict with file content and error if any
        """
        payload = {'path': path}
        response = requests.post(
            f'{self.base_url}/read_file',
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def delete_file(self, path: str) -> Dict[str, Any]:
        """
        Delete a file.
        
        Args:
            path: The file path to delete
            
        Returns:
            Dict with success status and error if any
        """
        payload = {'path': path}
        response = requests.post(
            f'{self.base_url}/delete_file',
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def make_dir(self, path: str) -> Dict[str, Any]:
        """
        Create a directory (including parent directories).
        
        Args:
            path: The directory path to create
            
        Returns:
            Dict with success status and error if any
        """
        payload = {'path': path}
        response = requests.post(
            f'{self.base_url}/make_dir',
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def delete_dir(self, path: str) -> Dict[str, Any]:
        """
        Recursively delete a directory and all its contents.
        
        Args:
            path: The directory path to delete
            
        Returns:
            Dict with success status and error if any
        """
        payload = {'path': path}
        response = requests.post(
            f'{self.base_url}/delete_dir',
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def list_dir(self, path: str) -> Dict[str, Any]:
        """
        List the contents of a directory.
        
        Args:
            path: The directory path to list
            
        Returns:
            Dict with entries list and error if any
        """
        payload = {'path': path}
        response = requests.post(
            f'{self.base_url}/list_dir',
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

