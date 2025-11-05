# coding: utf-8

"""
Filesystem operations for Koyeb Sandbox instances
Using SandboxClient HTTP API
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Union

from .executor_client import SandboxClient
from .utils import (
    SandboxError,
    check_error_message,
    create_sandbox_client,
    escape_shell_arg,
    run_sync_in_executor,
)

if TYPE_CHECKING:
    from .exec import SandboxExecutor
    from .sandbox import Sandbox


class SandboxFilesystemError(SandboxError):
    """Base exception for filesystem operations"""


class SandboxFileNotFoundError(SandboxFilesystemError):
    """Raised when file or directory not found"""


class SandboxFileExistsError(SandboxFilesystemError):
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

    def __init__(self, sandbox: Sandbox) -> None:
        self.sandbox = sandbox
        self._client = None
        self._executor = None

    def _get_client(self) -> SandboxClient:
        """Get or create SandboxClient instance"""
        if self._client is None:
            sandbox_url = self.sandbox._get_sandbox_url()
            self._client = create_sandbox_client(
                sandbox_url, self.sandbox.sandbox_secret
            )
        return self._client

    def _get_executor(self) -> "SandboxExecutor":
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
            response = client.write_file(path, content_str)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                raise SandboxFilesystemError(f"Failed to write file: {error_msg}")
        except Exception as e:
            if isinstance(e, SandboxFilesystemError):
                raise
            raise SandboxFilesystemError(f"Failed to write file: {str(e)}") from e

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
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"File not found: {path}")
                raise SandboxFilesystemError(f"Failed to read file: {error_msg}")
            content = response.get("content", "")
            return FileInfo(content=content, encoding=encoding)
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {path}") from e
            raise SandboxFilesystemError(f"Failed to read file: {error_msg}") from e

    def mkdir(self, path: str, recursive: bool = False) -> None:
        """
        Create a directory synchronously.

        Args:
            path: Absolute path to the directory
            recursive: Create parent directories if needed (default: False, not used - API always creates parents)
        """
        client = self._get_client()

        try:
            response = client.make_dir(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "FILE_EXISTS"):
                    raise SandboxFileExistsError(f"Directory already exists: {path}")
                raise SandboxFilesystemError(f"Failed to create directory: {error_msg}")
        except (SandboxFileExistsError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "FILE_EXISTS"):
                raise SandboxFileExistsError(f"Directory already exists: {path}") from e
            raise SandboxFilesystemError(
                f"Failed to create directory: {error_msg}"
            ) from e

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
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"Directory not found: {path}")
                raise SandboxFilesystemError(f"Failed to list directory: {error_msg}")
            entries = response.get("entries", [])
            return entries
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"Directory not found: {path}") from e
            raise SandboxFilesystemError(
                f"Failed to list directory: {error_msg}"
            ) from e

    def delete_file(self, path: str) -> None:
        """
        Delete a file synchronously.

        Args:
            path: Absolute path to the file
        """
        client = self._get_client()

        try:
            response = client.delete_file(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"File not found: {path}")
                raise SandboxFilesystemError(f"Failed to delete file: {error_msg}")
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {path}") from e
            raise SandboxFilesystemError(f"Failed to delete file: {error_msg}") from e

    def delete_dir(self, path: str) -> None:
        """
        Delete a directory synchronously.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_client()

        try:
            response = client.delete_dir(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"Directory not found: {path}")
                if check_error_message(error_msg, "DIR_NOT_EMPTY"):
                    raise SandboxFilesystemError(f"Directory not empty: {path}")
                raise SandboxFilesystemError(f"Failed to delete directory: {error_msg}")
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"Directory not found: {path}") from e
            if check_error_message(error_msg, "DIR_NOT_EMPTY"):
                raise SandboxFilesystemError(f"Directory not empty: {path}") from e
            raise SandboxFilesystemError(
                f"Failed to delete directory: {error_msg}"
            ) from e

    def rename_file(self, old_path: str, new_path: str) -> None:
        """
        Rename a file synchronously.

        Args:
            old_path: Current file path
            new_path: New file path
        """
        # Use exec since there's no direct rename in SandboxClient
        # Properly escape paths to prevent shell injection
        executor = self._get_executor()
        old_path_escaped = escape_shell_arg(old_path)
        new_path_escaped = escape_shell_arg(new_path)
        result = executor(f"mv {old_path_escaped} {new_path_escaped}")

        if not result.success:
            if check_error_message(result.stderr, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {old_path}")
            raise SandboxFilesystemError(f"Failed to rename file: {result.stderr}")

    def move_file(self, source_path: str, destination_path: str) -> None:
        """
        Move a file to a different directory synchronously.

        Args:
            source_path: Current file path
            destination_path: Destination path
        """
        # Use exec since there's no direct move in SandboxClient
        # Properly escape paths to prevent shell injection
        executor = self._get_executor()
        source_path_escaped = escape_shell_arg(source_path)
        destination_path_escaped = escape_shell_arg(destination_path)
        result = executor(f"mv {source_path_escaped} {destination_path_escaped}")

        if not result.success:
            if check_error_message(result.stderr, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {source_path}")
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
        path_escaped = escape_shell_arg(path)
        result = executor(f"test -e {path_escaped}")
        return result.success

    def is_file(self, path: str) -> bool:
        """Check if path is a file synchronously"""
        executor = self._get_executor()
        path_escaped = escape_shell_arg(path)
        result = executor(f"test -f {path_escaped}")
        return result.success

    def is_dir(self, path: str) -> bool:
        """Check if path is a directory synchronously"""
        executor = self._get_executor()
        path_escaped = escape_shell_arg(path)
        result = executor(f"test -d {path_escaped}")
        return result.success

    def upload_file(
        self, local_path: str, remote_path: str, encoding: str = "utf-8"
    ) -> None:
        """
        Upload a local file to the sandbox synchronously.

        Args:
            local_path: Path to the local file
            remote_path: Destination path in the sandbox
            encoding: File encoding (default: "utf-8"). Use "base64" for binary files.

        Raises:
            SandboxFileNotFoundError: If local file doesn't exist
            UnicodeDecodeError: If file cannot be decoded with specified encoding
        """
        if not os.path.exists(local_path):
            raise SandboxFileNotFoundError(f"Local file not found: {local_path}")

        with open(local_path, "rb") as f:
            content_bytes = f.read()

        if encoding == "base64":
            import base64

            content = base64.b64encode(content_bytes).decode("ascii")
            self.write_file(remote_path, content, encoding="base64")
        else:
            try:
                content = content_bytes.decode(encoding)
                self.write_file(remote_path, content, encoding=encoding)
            except UnicodeDecodeError as e:
                raise UnicodeDecodeError(
                    e.encoding,
                    e.object,
                    e.start,
                    e.end,
                    f"Cannot decode file as {encoding}. Use encoding='base64' for binary files.",
                ) from e

    def download_file(
        self, remote_path: str, local_path: str, encoding: str = "utf-8"
    ) -> None:
        """
        Download a file from the sandbox to a local path synchronously.

        Args:
            remote_path: Path to the file in the sandbox
            local_path: Destination path on the local filesystem
            encoding: File encoding (default: "utf-8"). Use "base64" for binary files.

        Raises:
            SandboxFileNotFoundError: If remote file doesn't exist
        """
        file_info = self.read_file(remote_path, encoding=encoding)

        if encoding == "base64":
            import base64

            content_bytes = base64.b64decode(file_info.content)
        else:
            content_bytes = file_info.content.encode(encoding)

        with open(local_path, "wb") as f:
            f.write(content_bytes)

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
        path_escaped = escape_shell_arg(path)

        if recursive:
            result = executor(f"rm -rf {path_escaped}")
        else:
            result = executor(f"rm {path_escaped}")

        if not result.success:
            if check_error_message(result.stderr, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {path}")
            raise SandboxFilesystemError(f"Failed to remove: {result.stderr}")

    def open(self, path: str, mode: str = "r") -> SandboxFileIO:
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

    async def _run_sync(self, method, *args, **kwargs):
        """
        Helper method to run a synchronous method in an executor.

        Args:
            method: The sync method to run (from super())
            *args: Positional arguments for the method
            **kwargs: Keyword arguments for the method

        Returns:
            Result of the synchronous method call
        """
        return await run_sync_in_executor(method, *args, **kwargs)

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
        await self._run_sync(super().write_file, path, content, encoding)

    async def read_file(self, path: str, encoding: str = "utf-8") -> FileInfo:
        """
        Read a file from the sandbox asynchronously.

        Args:
            path: Absolute path to the file
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.

        Returns:
            FileInfo: Object with content and encoding
        """
        return await self._run_sync(super().read_file, path, encoding)

    async def mkdir(self, path: str, recursive: bool = False) -> None:
        """
        Create a directory asynchronously.

        Args:
            path: Absolute path to the directory
            recursive: Create parent directories if needed (default: False, not used - API always creates parents)
        """
        await self._run_sync(super().mkdir, path, recursive)

    async def list_dir(self, path: str = ".") -> List[str]:
        """
        List contents of a directory asynchronously.

        Args:
            path: Path to the directory (default: current directory)

        Returns:
            List[str]: Names of files and directories within the specified path.
        """
        return await self._run_sync(super().list_dir, path)

    async def delete_file(self, path: str) -> None:
        """
        Delete a file asynchronously.

        Args:
            path: Absolute path to the file
        """
        await self._run_sync(super().delete_file, path)

    async def delete_dir(self, path: str) -> None:
        """
        Delete a directory asynchronously.

        Args:
            path: Absolute path to the directory
        """
        await self._run_sync(super().delete_dir, path)

    async def rename_file(self, old_path: str, new_path: str) -> None:
        """
        Rename a file asynchronously.

        Args:
            old_path: Current file path
            new_path: New file path
        """
        await self._run_sync(super().rename_file, old_path, new_path)

    async def move_file(self, source_path: str, destination_path: str) -> None:
        """
        Move a file to a different directory asynchronously.

        Args:
            source_path: Current file path
            destination_path: Destination path
        """
        await self._run_sync(super().move_file, source_path, destination_path)

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
        return await self._run_sync(super().exists, path)

    async def is_file(self, path: str) -> bool:
        """Check if path is a file asynchronously"""
        return await self._run_sync(super().is_file, path)

    async def is_dir(self, path: str) -> bool:
        """Check if path is a directory asynchronously"""
        return await self._run_sync(super().is_dir, path)

    async def upload_file(
        self, local_path: str, remote_path: str, encoding: str = "utf-8"
    ) -> None:
        """
        Upload a local file to the sandbox asynchronously.

        Args:
            local_path: Path to the local file
            remote_path: Destination path in the sandbox
            encoding: File encoding (default: "utf-8"). Use "base64" for binary files.
        """
        await self._run_sync(super().upload_file, local_path, remote_path, encoding)

    async def download_file(
        self, remote_path: str, local_path: str, encoding: str = "utf-8"
    ) -> None:
        """
        Download a file from the sandbox to a local path asynchronously.

        Args:
            remote_path: Path to the file in the sandbox
            local_path: Destination path on the local filesystem
            encoding: File encoding (default: "utf-8"). Use "base64" for binary files.
        """
        await self._run_sync(super().download_file, remote_path, local_path, encoding)

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
        await self._run_sync(super().rm, path, recursive)

    def open(self, path: str, mode: str = "r") -> AsyncSandboxFileIO:
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
            except SandboxFileNotFoundError:
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
            except SandboxFileNotFoundError:
                pass

        await self.filesystem.write_file(self.path, content)

    def close(self) -> None:
        """Close the file"""
        self._closed = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
