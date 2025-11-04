# coding: utf-8

"""
Filesystem operations for Koyeb Sandbox instances
Using SandboxClient HTTP API
"""

import asyncio
import os
from dataclasses import dataclass
from typing import Dict, List, Union

from .executor_client import SandboxClient
from .utils import SandboxError


class SandboxFilesystemError(SandboxError):
    """Base exception for filesystem operations"""


class FileNotFoundError(SandboxFilesystemError):
    """Raised when file or directory not found"""


class FileExistsError(SandboxFilesystemError):
    """Raised when file already exists"""


@dataclass
class FileInfo:
    """File information"""

    content: str
    encoding: str


class SandboxFilesystem:
    """
    Synchronous filesystem operations for Koyeb Sandbox instances.
    Using SandboxClient HTTP API.

    For async usage, use AsyncSandboxFilesystem instead.
    """

    def __init__(self, sandbox):
        self.sandbox = sandbox
        self._client = None
        self._executor = None

    def _get_client(self) -> SandboxClient:
        """Get or create SandboxClient instance"""
        if self._client is None:
            sandbox_url = self.sandbox.get_sandbox_url()
            if not sandbox_url:
                raise SandboxError("Unable to get sandbox URL")
            if not self.sandbox.sandbox_secret:
                raise SandboxError("Sandbox secret not available")
            self._client = SandboxClient(sandbox_url, self.sandbox.sandbox_secret)
        return self._client

    def _get_executor(self):
        """Get or create SandboxExecutor instance"""
        if self._executor is None:
            from .exec import SandboxExecutor

            self._executor = SandboxExecutor(self.sandbox)
        return self._executor

    def write_file(
        self, path: str, content: Union[str, bytes], encoding: str = "utf-8"
    ) -> None:
        """
        Write content to a file synchronously.

        Args:
            path: Absolute path to the file
            content: Content to write (string or bytes)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.
        """
        client = self._get_client()

        if isinstance(content, bytes):
            content_str = content.decode("utf-8")
        else:
            content_str = content

        try:
            client.write_file(path, content_str)
        except Exception as e:
            raise SandboxFilesystemError(f"Failed to write file: {str(e)}")

    def read_file(self, path: str, encoding: str = "utf-8") -> FileInfo:
        """
        Read a file from the sandbox synchronously.

        Args:
            path: Absolute path to the file
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.

        Returns:
            FileInfo: Object with content and encoding
        """
        client = self._get_client()

        try:
            response = client.read_file(path)
            content = response.get("content", "")
            return FileInfo(content=content, encoding=encoding)
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg.lower():
                raise FileNotFoundError(f"File not found: {path}")
            raise SandboxFilesystemError(f"Failed to read file: {error_msg}")

    def mkdir(self, path: str, recursive: bool = False) -> None:
        """
        Create a directory synchronously.

        Args:
            path: Absolute path to the directory
            recursive: Create parent directories if needed (default: False, not used - API always creates parents)
        """
        client = self._get_client()

        try:
            client.make_dir(path)
        except Exception as e:
            error_msg = str(e)
            if "exists" in error_msg.lower():
                raise FileExistsError(f"Directory already exists: {path}")
            raise SandboxFilesystemError(f"Failed to create directory: {error_msg}")

    def list_dir(self, path: str = ".") -> List[str]:
        """
        List contents of a directory synchronously.

        Args:
            path: Path to the directory (default: current directory)

        Returns:
            List[str]: Names of files and directories within the specified path.
        """
        client = self._get_client()

        try:
            response = client.list_dir(path)
            entries = response.get("entries", [])
            return entries
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg.lower():
                raise FileNotFoundError(f"Directory not found: {path}")
            raise SandboxFilesystemError(f"Failed to list directory: {error_msg}")

    def delete_file(self, path: str) -> None:
        """
        Delete a file synchronously.

        Args:
            path: Absolute path to the file
        """
        client = self._get_client()

        try:
            client.delete_file(path)
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg.lower():
                raise FileNotFoundError(f"File not found: {path}")
            raise SandboxFilesystemError(f"Failed to delete file: {error_msg}")

    def delete_dir(self, path: str) -> None:
        """
        Delete a directory synchronously.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_client()

        try:
            client.delete_dir(path)
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg.lower():
                raise FileNotFoundError(f"Directory not found: {path}")
            if "not empty" in error_msg.lower():
                raise SandboxFilesystemError(f"Directory not empty: {path}")
            raise SandboxFilesystemError(f"Failed to delete directory: {error_msg}")

    def rename_file(self, old_path: str, new_path: str) -> None:
        """
        Rename a file synchronously.

        Args:
            old_path: Current file path
            new_path: New file path
        """
        # Use exec since there's no direct rename in SandboxClient
        executor = self._get_executor()
        result = executor(f"mv {old_path} {new_path}")

        if not result.success:
            if "No such file" in result.stderr:
                raise FileNotFoundError(f"File not found: {old_path}")
            raise SandboxFilesystemError(f"Failed to rename file: {result.stderr}")

    def move_file(self, source_path: str, destination_path: str) -> None:
        """
        Move a file to a different directory synchronously.

        Args:
            source_path: Current file path
            destination_path: Destination path
        """
        # Use exec since there's no direct move in SandboxClient
        executor = self._get_executor()
        result = executor(f"mv {source_path} {destination_path}")

        if not result.success:
            if "No such file" in result.stderr:
                raise FileNotFoundError(f"File not found: {source_path}")
            raise SandboxFilesystemError(f"Failed to move file: {result.stderr}")

    def write_files(self, files: List[Dict[str, str]]) -> None:
        """
        Write multiple files in a single operation synchronously.

        Args:
            files: List of dictionaries, each with 'path', 'content', and optional 'encoding'.
        """
        for file_info in files:
            path = file_info["path"]
            content = file_info["content"]
            encoding = file_info.get("encoding", "utf-8")
            self.write_file(path, content, encoding)

    def exists(self, path: str) -> bool:
        """Check if file/directory exists synchronously"""
        executor = self._get_executor()
        result = executor(f"test -e {path}")
        return result.success

    def is_file(self, path: str) -> bool:
        """Check if path is a file synchronously"""
        executor = self._get_executor()
        result = executor(f"test -f {path}")
        return result.success

    def is_dir(self, path: str) -> bool:
        """Check if path is a directory synchronously"""
        executor = self._get_executor()
        result = executor(f"test -d {path}")
        return result.success

    def upload_file(self, local_path: str, remote_path: str) -> None:
        """
        Upload a local file to the sandbox synchronously.

        Args:
            local_path: Path to the local file
            remote_path: Destination path in the sandbox
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found: {local_path}")

        with open(local_path, "rb") as f:
            content = f.read().decode("utf-8")

        self.write_file(remote_path, content)

    def download_file(self, remote_path: str, local_path: str) -> None:
        """
        Download a file from the sandbox to a local path synchronously.

        Args:
            remote_path: Path to the file in the sandbox
            local_path: Destination path on the local filesystem
        """
        file_info = self.read_file(remote_path)
        content = file_info.content.encode("utf-8")

        with open(local_path, "wb") as f:
            f.write(content)

    def ls(self, path: str = ".") -> List[str]:
        """
        List directory contents synchronously.

        Args:
            path: Path to list

        Returns:
            List of file/directory names
        """
        return self.list_dir(path)

    def rm(self, path: str, recursive: bool = False) -> None:
        """
        Remove file or directory synchronously.

        Args:
            path: Path to remove
            recursive: Remove recursively
        """
        executor = self._get_executor()

        if recursive:
            result = executor(f"rm -rf {path}")
        else:
            result = executor(f"rm {path}")

        if not result.success:
            if "No such file or directory" in result.stderr:
                raise FileNotFoundError(f"File not found: {path}")
            raise SandboxFilesystemError(f"Failed to remove: {result.stderr}")

    def open(self, path: str, mode: str = "r") -> "SandboxFileIO":
        """
        Open a file in the sandbox synchronously.

        Args:
            path: Path to the file
            mode: Open mode ('r', 'w', 'a', etc.)

        Returns:
            SandboxFileIO: File handle
        """
        return SandboxFileIO(self, path, mode)


class AsyncSandboxFilesystem(SandboxFilesystem):
    """
    Async filesystem operations for Koyeb Sandbox instances.
    Inherits from SandboxFilesystem and provides async methods.
    """

    async def write_file(
        self, path: str, content: Union[str, bytes], encoding: str = "utf-8"
    ) -> None:
        """
        Write content to a file asynchronously.

        Args:
            path: Absolute path to the file
            content: Content to write (string or bytes)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            lambda: super(AsyncSandboxFilesystem, self).write_file(
                path, content, encoding
            ),
        )

    async def read_file(self, path: str, encoding: str = "utf-8") -> FileInfo:
        """
        Read a file from the sandbox asynchronously.

        Args:
            path: Absolute path to the file
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.

        Returns:
            FileInfo: Object with content and encoding
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, lambda: super(AsyncSandboxFilesystem, self).read_file(path, encoding)
        )

    async def mkdir(self, path: str, recursive: bool = False) -> None:
        """
        Create a directory asynchronously.

        Args:
            path: Absolute path to the directory
            recursive: Create parent directories if needed (default: False, not used - API always creates parents)
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None, lambda: super(AsyncSandboxFilesystem, self).mkdir(path, recursive)
        )

    async def list_dir(self, path: str = ".") -> List[str]:
        """
        List contents of a directory asynchronously.

        Args:
            path: Path to the directory (default: current directory)

        Returns:
            List[str]: Names of files and directories within the specified path.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, lambda: super(AsyncSandboxFilesystem, self).list_dir(path)
        )

    async def delete_file(self, path: str) -> None:
        """
        Delete a file asynchronously.

        Args:
            path: Absolute path to the file
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None, lambda: super(AsyncSandboxFilesystem, self).delete_file(path)
        )

    async def delete_dir(self, path: str) -> None:
        """
        Delete a directory asynchronously.

        Args:
            path: Absolute path to the directory
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None, lambda: super(AsyncSandboxFilesystem, self).delete_dir(path)
        )

    async def rename_file(self, old_path: str, new_path: str) -> None:
        """
        Rename a file asynchronously.

        Args:
            old_path: Current file path
            new_path: New file path
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            lambda: super(AsyncSandboxFilesystem, self).rename_file(old_path, new_path),
        )

    async def move_file(self, source_path: str, destination_path: str) -> None:
        """
        Move a file to a different directory asynchronously.

        Args:
            source_path: Current file path
            destination_path: Destination path
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            lambda: super(AsyncSandboxFilesystem, self).move_file(
                source_path, destination_path
            ),
        )

    async def write_files(self, files: List[Dict[str, str]]) -> None:
        """
        Write multiple files in a single operation asynchronously.

        Args:
            files: List of dictionaries, each with 'path', 'content', and optional 'encoding'.
        """
        for file_info in files:
            path = file_info["path"]
            content = file_info["content"]
            encoding = file_info.get("encoding", "utf-8")
            await self.write_file(path, content, encoding)

    async def exists(self, path: str) -> bool:
        """Check if file/directory exists asynchronously"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, lambda: super(AsyncSandboxFilesystem, self).exists(path)
        )

    async def is_file(self, path: str) -> bool:
        """Check if path is a file asynchronously"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, lambda: super(AsyncSandboxFilesystem, self).is_file(path)
        )

    async def is_dir(self, path: str) -> bool:
        """Check if path is a directory asynchronously"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, lambda: super(AsyncSandboxFilesystem, self).is_dir(path)
        )

    async def upload_file(self, local_path: str, remote_path: str) -> None:
        """
        Upload a local file to the sandbox asynchronously.

        Args:
            local_path: Path to the local file
            remote_path: Destination path in the sandbox
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            lambda: super(AsyncSandboxFilesystem, self).upload_file(
                local_path, remote_path
            ),
        )

    async def download_file(self, remote_path: str, local_path: str) -> None:
        """
        Download a file from the sandbox to a local path asynchronously.

        Args:
            remote_path: Path to the file in the sandbox
            local_path: Destination path on the local filesystem
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            lambda: super(AsyncSandboxFilesystem, self).download_file(
                remote_path, local_path
            ),
        )

    async def ls(self, path: str = ".") -> List[str]:
        """
        List directory contents asynchronously.

        Args:
            path: Path to list

        Returns:
            List of file/directory names
        """
        return await self.list_dir(path)

    async def rm(self, path: str, recursive: bool = False) -> None:
        """
        Remove file or directory asynchronously.

        Args:
            path: Path to remove
            recursive: Remove recursively
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None, lambda: super(AsyncSandboxFilesystem, self).rm(path, recursive)
        )

    def open(self, path: str, mode: str = "r") -> "AsyncSandboxFileIO":
        """
        Open a file in the sandbox asynchronously.

        Args:
            path: Path to the file
            mode: Open mode ('r', 'w', 'a', etc.)

        Returns:
            AsyncSandboxFileIO: Async file handle
        """
        return AsyncSandboxFileIO(self, path, mode)


class SandboxFileIO:
    """Synchronous file I/O handle for sandbox files"""

    def __init__(self, filesystem: SandboxFilesystem, path: str, mode: str):
        self.filesystem = filesystem
        self.path = path
        self.mode = mode
        self._closed = False

    def read(self) -> str:
        """Read file content synchronously"""
        if "r" not in self.mode:
            raise ValueError("File not opened for reading")

        if self._closed:
            raise ValueError("File is closed")

        file_info = self.filesystem.read_file(self.path)
        return file_info.content

    def write(self, content: str) -> None:
        """Write content to file synchronously"""
        if "w" not in self.mode and "a" not in self.mode:
            raise ValueError("File not opened for writing")

        if self._closed:
            raise ValueError("File is closed")

        if "a" in self.mode:
            try:
                existing = self.filesystem.read_file(self.path)
                content = existing.content + content
            except FileNotFoundError:
                pass

        self.filesystem.write_file(self.path, content)

    def close(self) -> None:
        """Close the file"""
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncSandboxFileIO:
    """Async file I/O handle for sandbox files"""

    def __init__(self, filesystem: AsyncSandboxFilesystem, path: str, mode: str):
        self.filesystem = filesystem
        self.path = path
        self.mode = mode
        self._closed = False

    async def read(self) -> str:
        """Read file content asynchronously"""
        if "r" not in self.mode:
            raise ValueError("File not opened for reading")

        if self._closed:
            raise ValueError("File is closed")

        file_info = await self.filesystem.read_file(self.path)
        return file_info.content

    async def write(self, content: str) -> None:
        """Write content to file asynchronously"""
        if "w" not in self.mode and "a" not in self.mode:
            raise ValueError("File not opened for writing")

        if self._closed:
            raise ValueError("File is closed")

        if "a" in self.mode:
            try:
                existing = await self.filesystem.read_file(self.path)
                content = existing.content + content
            except FileNotFoundError:
                pass

        await self.filesystem.write_file(self.path, content)

    def close(self) -> None:
        """Close the file"""
        self._closed = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
