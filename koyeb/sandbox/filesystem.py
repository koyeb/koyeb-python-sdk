# coding: utf-8

"""
Filesystem operations for Koyeb Sandbox instances
Using SandboxClient HTTP API
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import shlex
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    AsyncIterator,
    BinaryIO,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Union,
)

from .executor_client import AsyncSandboxClient, SandboxClient
from .errors import (
    SandboxError,
    SandboxRequestError,
    SandboxServiceError,
)

if TYPE_CHECKING:
    from .exec import AsyncSandboxExecutor, SandboxExecutor
    from .sandbox import Sandbox


ERROR_MESSAGES = {
    "NO_SUCH_FILE": ["No such file", "not found", "No such file or directory"],
    "FILE_EXISTS": ["exists", "already exists"],
    "DIR_NOT_EMPTY": ["not empty", "Directory not empty"],
}


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


def escape_shell_arg(arg: str) -> str:
    """
    Escape a shell argument for safe use in shell commands.

    Args:
        arg: The argument to escape

    Returns:
        Properly escaped shell argument
    """
    return shlex.quote(arg)


class SandboxFilesystemError(SandboxError):
    """Base exception for filesystem operations"""


class SandboxFileNotFoundError(SandboxFilesystemError):
    """Raised when file or directory not found"""


class SandboxFileExistsError(SandboxFilesystemError):
    """Raised when file already exists"""


def _executor_error(
    error_msg: str,
    what: str,
    not_found_msg: Optional[str] = None,
    exists_msg: Optional[str] = None,
    not_empty_msg: Optional[str] = None,
) -> SandboxFilesystemError:
    """The one place executor error strings classify into the SDK taxonomy.

    Typed subclasses map only where the operation makes sense; message
    text stays the historical wording.
    """
    if not_found_msg and check_error_message(error_msg, "NO_SUCH_FILE"):
        return SandboxFileNotFoundError(not_found_msg)
    if exists_msg and check_error_message(error_msg, "FILE_EXISTS"):
        return SandboxFileExistsError(exists_msg)
    if not_empty_msg and check_error_message(error_msg, "DIR_NOT_EMPTY"):
        return SandboxFilesystemError(not_empty_msg)
    return SandboxFilesystemError(f"Failed to {what}: {error_msg}")


def _put_body(
    content: Union[str, bytes, BinaryIO, Iterable[bytes]], encoding: str
) -> Union[bytes, BinaryIO, Iterable[bytes]]:
    """Content to send on the streamed /files routes: real bytes on disk.

    encoding="base64" is a transport detail: the content is base64 text and
    the decoded bytes land on disk — the documented behavior change vs the
    legacy routes, which wrote the base64 text itself.
    """
    if isinstance(content, str):
        if encoding == "base64":
            return base64.b64decode(content)
        return content.encode(encoding)
    if isinstance(content, bytes) and encoding == "base64":
        return base64.b64decode(content)
    return content


def _read_content(raw: bytes, encoding: Optional[str]) -> Union[str, bytes]:
    """Interpret raw file bytes per the requested encoding (streamed routes)."""
    if encoding is None:
        return raw
    if encoding == "base64":
        return base64.b64encode(raw).decode("ascii")
    return raw.decode(encoding)


def _files_error(
    e: SandboxRequestError, what: str, path: str
) -> SandboxFilesystemError:
    """A streamed-route status error classified into the filesystem taxonomy.

    The /files routes answer with real status codes: the code is the
    contract, the JSON body's error text only adds detail.
    """
    msg = ""
    try:
        msg = json.loads(e.body).get("error", "") if e.body else ""
    except (AttributeError, ValueError):
        pass
    if e.status_code == 404:
        return SandboxFileNotFoundError(f"File not found: {path}")
    if e.status_code == 409:
        return SandboxFileExistsError(msg or f"Conflict at: {path}")
    detail = msg or (e.body if e.body else f"HTTP {e.status_code}")
    return SandboxFilesystemError(f"Failed to {what}: {detail}")


@contextmanager
def _translating_files_errors(what: str, path: str):
    """Translate streamed-route failures once, for every filesystem operation.

    Real status codes classify through _files_error; anything else wraps as
    "Failed to <what>" — the filesystem taxonomy is what callers catch.
    """
    try:
        yield
    except SandboxServiceError:
        raise
    except SandboxRequestError as e:
        raise _files_error(e, what, path) from e
    except SandboxFilesystemError:
        raise
    except Exception as e:
        raise SandboxFilesystemError(f"Failed to {what}: {str(e)}") from e


class _ProgressReporter:
    """progress(done, total) at most every 100 ms, plus a guaranteed final call."""

    def __init__(self, progress: Optional[Callable[[int, int], None]], total: int):
        self._progress = progress
        self._total = total
        self._last_time = 0.0
        self._last_done = None

    def update(self, done: int) -> None:
        if self._progress is None:
            return
        now = time.monotonic()
        if now - self._last_time >= 0.1:
            self._progress(done, self._total)
            self._last_time = now
            self._last_done = done

    def finish(self, done: int) -> None:
        if self._progress is not None and done != self._last_done:
            self._progress(done, self._total)


def _file_sha256(path: str) -> str:
    """sha256 of a local file, constant memory.

    A first pass before the streamed upload: the digest travels in the
    X-Content-SHA256 header, which precedes the body on the wire.
    """
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _progress_chunks(
    stream, reporter: _ProgressReporter, chunk_size: int = 65536
) -> Iterator[bytes]:
    """Read a binary stream in chunks, reporting progress as they go."""
    done = 0
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        done += len(chunk)
        reporter.update(done)
        yield chunk
    reporter.finish(done)


@dataclass
class FileInfo:
    """File information"""

    content: Union[str, bytes]
    encoding: Optional[str]


@dataclass
class FileStat:
    """File metadata from the streamed /files/stat route (executor v0.0.24+).

    type is one of file|dir|symlink|other; mode is the octal permission
    string (e.g. "0644"); mtime is RFC 3339 UTC with nanoseconds.
    """

    type: str
    size: int
    mode: str
    mtime: str
    sha256: Optional[str] = None


class SandboxFilesystem:
    """
    Synchronous filesystem operations for Koyeb Sandbox instances.
    Using SandboxClient HTTP API.

    For async usage, use AsyncSandboxFilesystem instead.
    """

    def __init__(self, sandbox: Sandbox) -> None:
        self.sandbox = sandbox
        self._executor = None

    def _get_client(self) -> SandboxClient:
        """Get or create SandboxClient instance, shared with the sandbox"""
        return self.sandbox._get_client()

    def _get_executor(self) -> "SandboxExecutor":
        """Get or create SandboxExecutor instance"""
        if self._executor is None:
            from .exec import SandboxExecutor

            self._executor = SandboxExecutor(self.sandbox)
        return self._executor

    def write_file(
        self,
        path: str,
        content: Union[str, bytes, BinaryIO, Iterable[bytes]],
        encoding: str = "utf-8",
        *,
        mode: Optional[str] = None,
    ) -> None:
        """
        Write content to a file synchronously.

        On executors v0.0.24+ the content streams through PUT /files,
        binary-safe: any byte sequence lands on disk as-is.
        encoding="base64" decodes str and bytes content to the real
        bytes; BinaryIO and iterables stream as-is, ignoring it. Older
        executors are detected once per handle and keep the legacy JSON behavior —
        which cannot carry streamed content (BinaryIO, an iterable of
        chunks): that raises and names v0.0.24.

        Args:
            path: Absolute path to the file
            content: Content to write — string, bytes, a file object or an
                iterable of bytes chunks (the last two require executor
                v0.0.24+)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.
            mode: Octal permission string, e.g. "0644" (streamed routes only;
                the legacy routes keep the destination's mode)
        """
        client = self._get_client()

        if client.has_files_routes():
            with _translating_files_errors("write file", path):
                client.files_put(path, _put_body(content, encoding), mode=mode)
            return

        if not isinstance(content, (str, bytes)):
            raise SandboxFilesystemError(
                "streamed content (BinaryIO or an iterable of chunks) requires "
                "the streamed /files routes (executor v0.0.24+)"
            )
        if isinstance(content, bytes):
            if encoding == "base64":
                content_str = base64.b64encode(content).decode("ascii")
            else:
                content_str = content.decode(encoding)
        else:
            content_str = content

        try:
            response = client.write_file(path, content_str)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"), "write file"
                )
        except (SandboxServiceError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise SandboxFilesystemError(f"Failed to write file: {str(e)}") from e

    def read_file(self, path: str, encoding: Optional[str] = "utf-8") -> FileInfo:
        """
        Read a file from the sandbox synchronously.

        On executors v0.0.24+ the bytes stream from GET /files,
        binary-safe: encoding=None returns the disk bytes, and
        encoding="base64" encodes the real bytes for transport. Older
        executors keep the legacy JSON behavior: encoding="base64"
        decodes the file's base64 text and returns bytes; encoding=None
        is not supported there and raises.

        Args:
            path: Absolute path to the file
            encoding: File encoding (default: "utf-8"). Streamed routes:
                None returns the disk bytes, "base64" encodes them.
                Legacy routes: "base64" decodes the file's base64 text;
                None raises.

        Returns:
            FileInfo: Object with content (str or bytes) and encoding
        """
        client = self._get_client()

        if client.has_files_routes():
            with _translating_files_errors("read file", path):
                raw = b"".join(client.files_read(path))
            return FileInfo(content=_read_content(raw, encoding), encoding=encoding)

        if encoding is None:
            raise SandboxFilesystemError(
                "reading raw bytes (encoding=None) requires the streamed "
                "/files routes (executor v0.0.24+)"
            )

        try:
            response = client.read_file(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "read file",
                    not_found_msg=f"File not found: {path}",
                )
            content_str = response.get("content", "")
            if encoding == "base64":
                content: Union[str, bytes] = base64.b64decode(content_str)
            else:
                content = content_str
            return FileInfo(content=content, encoding=encoding)
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "read file", not_found_msg=f"File not found: {path}"
            ) from e

    def open_read(self, path: str) -> Iterator[bytes]:
        """
        Stream a file's bytes from the sandbox, chunk by chunk.

        Constant memory on both sides (executor v0.0.24+). On legacy
        executors the file is read once as text and yielded as a single
        chunk — binary-safe streaming is not available there.

        Args:
            path: Absolute path to the file

        Yields:
            File content chunks
        """
        client = self._get_client()
        if not client.has_files_routes():
            yield self.read_file(path).content.encode("utf-8")
            return
        with _translating_files_errors("read file", path):
            for chunk in client.files_read(path):
                yield chunk

    def stat(self, path: str) -> FileStat:
        """
        Stat a file on the sandbox (executor v0.0.24+).

        Legacy executors have no stat route: this raises. Size comes from
        the filesystem, never from a HEAD — size-0 pseudo-files (e.g. under
        /proc) carry no length but have content.

        Args:
            path: Absolute path to the file

        Returns:
            FileStat with type (file|dir|symlink|other), size, mode (octal
            string) and mtime (RFC 3339 UTC, nanoseconds)
        """
        client = self._get_client()
        if not client.has_files_routes():
            raise SandboxFilesystemError(
                "stat requires the streamed /files routes (executor v0.0.24+)"
            )
        with _translating_files_errors("stat file", path):
            entry = client.files_stat(path)
            return FileStat(
                type=entry["type"],
                size=entry["size"],
                mode=entry["mode"],
                mtime=entry["mtime"],
                sha256=entry.get("sha256"),
            )

    def mkdir(self, path: str) -> None:
        """
        Create a directory synchronously.

        Note: Parent directories are always created automatically by the API.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_client()

        try:
            response = client.make_dir(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "create directory",
                    exists_msg=f"Directory already exists: {path}",
                )
        except (SandboxServiceError, SandboxFileExistsError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e),
                "create directory",
                exists_msg=f"Directory already exists: {path}",
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
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "list directory",
                    not_found_msg=f"Directory not found: {path}",
                )
            entries = response.get("entries", [])
            return entries
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "list directory", not_found_msg=f"Directory not found: {path}"
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
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "delete file",
                    not_found_msg=f"File not found: {path}",
                )
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "delete file", not_found_msg=f"File not found: {path}"
            ) from e

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
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "delete directory",
                    not_found_msg=f"Directory not found: {path}",
                    not_empty_msg=f"Directory not empty: {path}",
                )
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e),
                "delete directory",
                not_found_msg=f"Directory not found: {path}",
                not_empty_msg=f"Directory not empty: {path}",
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
            raise _executor_error(
                result.stderr,
                "rename file",
                not_found_msg=f"File not found: {old_path}",
            )

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
            raise _executor_error(
                result.stderr,
                "move file",
                not_found_msg=f"File not found: {source_path}",
            )

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
            SandboxFilesystem.write_file(self, path, content, encoding)

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
        self,
        local_path: str,
        remote_path: str,
        encoding: str = "utf-8",
        *,
        progress: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        """
        Upload a local file to the sandbox synchronously.

        On executors v0.0.24+ the file streams from disk through PUT
        /files — binary-safe, constant memory — with optional progress
        callbacks. Older executors keep the legacy JSON behavior (the
        encoding parameter applies there only).

        Args:
            local_path: Path to the local file
            remote_path: Destination path in the sandbox
            encoding: Legacy executors only (default: "utf-8"); the
                streamed routes are binary-safe and ignore it
            progress: Optional callback(done, total), called at most every
                100 ms during the transfer plus a final call

        The transfer is bounded by a 60 s idle timeout only; a per-call
        timeout override parameter is planned with the multipart slice.

        Raises:
            SandboxFileNotFoundError: If local file doesn't exist
        """
        if not os.path.exists(local_path):
            raise SandboxFileNotFoundError(f"Local file not found: {local_path}")

        client = self._get_client()
        if client.has_files_routes():
            reporter = _ProgressReporter(progress, os.path.getsize(local_path))
            with _translating_files_errors("upload file", remote_path):
                digest = _file_sha256(local_path)
                with open(local_path, "rb") as f:
                    reply = client.files_put(
                        remote_path,
                        _progress_chunks(f, reporter),
                        sha256=digest,
                    )
                if reply["sha256"] != digest:
                    raise SandboxFilesystemError(
                        f"Upload corrupted in transit: executor sha256 "
                        f"{reply['sha256']} != {digest}"
                    )
            return

        with open(local_path, "rb") as f:
            content_bytes = f.read()

        self.write_file(remote_path, content_bytes, encoding=encoding)

    def download_file(
        self,
        remote_path: str,
        local_path: str,
        encoding: str = "utf-8",
        *,
        progress: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        """
        Download a file from the sandbox to a local path synchronously.

        On executors v0.0.24+ the size comes from stat (never a HEAD), the
        bytes stream into <local>.part and rename into place on success:
        a failed download leaves the destination exactly as it was.
        Older executors keep the legacy JSON behavior.

        Args:
            remote_path: Path to the file in the sandbox
            local_path: Destination path on the local filesystem
            encoding: Legacy executors only (default: "utf-8"); the
                streamed routes are binary-safe and ignore it
            progress: Optional callback(done, total), called at most every
                100 ms during the transfer plus a final call

        The transfer is bounded by a 60 s idle timeout only; a per-call
        timeout override parameter is planned with the multipart slice.

        Raises:
            SandboxFileNotFoundError: If remote file doesn't exist
        """
        client = self._get_client()
        if client.has_files_routes():
            part_path = f"{local_path}.part"
            with _translating_files_errors("download file", remote_path):
                entry = client.files_stat(remote_path)
                reporter = _ProgressReporter(progress, entry["size"])
                done = 0
                renamed = False
                try:
                    with open(part_path, "wb") as out:
                        for chunk in client.files_read(remote_path):
                            out.write(chunk)
                            done += len(chunk)
                            reporter.update(done)
                    reporter.finish(done)
                    os.replace(part_path, local_path)
                    renamed = True
                finally:
                    if not renamed:
                        try:
                            os.unlink(part_path)
                        except OSError:
                            pass
            return

        file_info = self.read_file(remote_path, encoding=encoding)

        if isinstance(file_info.content, bytes):
            content_bytes = file_info.content
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
        return SandboxFilesystem.list_dir(self, path)

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
            raise _executor_error(
                result.stderr, "remove", not_found_msg=f"File not found: {path}"
            )

    def open(
        self, path: str, mode: str = "r", encoding: str = "utf-8"
    ) -> SandboxFileIO:
        """
        Open a file in the sandbox synchronously.

        Args:
            path: Path to the file
            mode: Open mode ('r', 'w', 'a', etc.)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.

        Returns:
            SandboxFileIO: File handle
        """
        return SandboxFileIO(self, path, mode, encoding)


class AsyncSandboxFilesystem(SandboxFilesystem):
    """
    Async filesystem operations for Koyeb Sandbox instances.
    Uses native async I/O via AsyncSandboxClient.
    """

    def _get_async_client(self) -> AsyncSandboxClient:
        """Get AsyncSandboxClient instance from the sandbox."""
        return self.sandbox._get_async_client()

    def _get_async_executor(self) -> "AsyncSandboxExecutor":
        """Get or create AsyncSandboxExecutor instance."""
        if self._executor is None:
            from .exec import AsyncSandboxExecutor

            self._executor = AsyncSandboxExecutor(self.sandbox)
        return self._executor

    async def write_file(
        self,
        path: str,
        content: Union[str, bytes, BinaryIO, Iterable[bytes]],
        encoding: str = "utf-8",
        *,
        mode: Optional[str] = None,
    ) -> None:
        """
        Write content to a file asynchronously.

        On executors v0.0.24+ the content streams through PUT /files,
        binary-safe: any byte sequence lands on disk as-is.
        encoding="base64" decodes str and bytes content to the real
        bytes; BinaryIO and iterables stream as-is, ignoring it. Older
        executors are detected once per handle and keep the legacy JSON behavior —
        which cannot carry streamed content (BinaryIO, an iterable of
        chunks): that raises and names v0.0.24.

        Args:
            path: Absolute path to the file
            content: Content to write — string, bytes, a file object or an
                iterable of bytes chunks (the last two require executor
                v0.0.24+)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.
            mode: Octal permission string, e.g. "0644" (streamed routes only;
                the legacy routes keep the destination's mode)
        """
        client = self._get_async_client()

        if await client.has_files_routes():
            with _translating_files_errors("write file", path):
                await client.files_put(path, _put_body(content, encoding), mode=mode)
            return

        if not isinstance(content, (str, bytes)):
            raise SandboxFilesystemError(
                "streamed content (BinaryIO or an iterable of chunks) requires "
                "the streamed /files routes (executor v0.0.24+)"
            )
        if isinstance(content, bytes):
            if encoding == "base64":
                content_str = base64.b64encode(content).decode("ascii")
            else:
                content_str = content.decode(encoding)
        else:
            content_str = content

        try:
            response = await client.write_file(path, content_str)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"), "write file"
                )
        except (SandboxServiceError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise SandboxFilesystemError(f"Failed to write file: {str(e)}") from e

    async def read_file(self, path: str, encoding: Optional[str] = "utf-8") -> FileInfo:
        """
        Read a file from the sandbox asynchronously.

        On executors v0.0.24+ the bytes stream from GET /files,
        binary-safe: encoding=None returns the disk bytes, and
        encoding="base64" encodes the real bytes for transport. Older
        executors keep the legacy JSON behavior: encoding="base64"
        decodes the file's base64 text and returns bytes; encoding=None
        is not supported there and raises.

        Args:
            path: Absolute path to the file
            encoding: File encoding (default: "utf-8"). Streamed routes:
                None returns the disk bytes, "base64" encodes them.
                Legacy routes: "base64" decodes the file's base64 text;
                None raises.

        Returns:
            FileInfo: Object with content (str or bytes) and encoding
        """
        client = self._get_async_client()

        if await client.has_files_routes():
            with _translating_files_errors("read file", path):
                chunks = []
                async for chunk in client.files_read(path):
                    chunks.append(chunk)
                raw = b"".join(chunks)
            return FileInfo(content=_read_content(raw, encoding), encoding=encoding)

        if encoding is None:
            raise SandboxFilesystemError(
                "reading raw bytes (encoding=None) requires the streamed "
                "/files routes (executor v0.0.24+)"
            )

        try:
            response = await client.read_file(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "read file",
                    not_found_msg=f"File not found: {path}",
                )
            content_str = response.get("content", "")
            if encoding == "base64":
                content: Union[str, bytes] = base64.b64decode(content_str)
            else:
                content = content_str
            return FileInfo(content=content, encoding=encoding)
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "read file", not_found_msg=f"File not found: {path}"
            ) from e

    async def open_read(self, path: str) -> AsyncIterator[bytes]:
        """
        Stream a file's bytes from the sandbox, chunk by chunk.

        Constant memory on both sides (executor v0.0.24+). On legacy
        executors the file is read once as text and yielded as a single
        chunk — binary-safe streaming is not available there.

        Args:
            path: Absolute path to the file

        Yields:
            File content chunks
        """
        client = self._get_async_client()
        if not await client.has_files_routes():
            yield (await self.read_file(path)).content.encode("utf-8")
            return
        with _translating_files_errors("read file", path):
            async for chunk in client.files_read(path):
                yield chunk

    async def stat(self, path: str) -> FileStat:
        """
        Stat a file on the sandbox (executor v0.0.24+).

        Legacy executors have no stat route: this raises. Size comes from
        the filesystem, never from a HEAD — size-0 pseudo-files (e.g. under
        /proc) carry no length but have content.

        Args:
            path: Absolute path to the file

        Returns:
            FileStat with type (file|dir|symlink|other), size, mode (octal
            string) and mtime (RFC 3339 UTC, nanoseconds)
        """
        client = self._get_async_client()
        if not await client.has_files_routes():
            raise SandboxFilesystemError(
                "stat requires the streamed /files routes (executor v0.0.24+)"
            )
        with _translating_files_errors("stat file", path):
            entry = await client.files_stat(path)
            return FileStat(
                type=entry["type"],
                size=entry["size"],
                mode=entry["mode"],
                mtime=entry["mtime"],
                sha256=entry.get("sha256"),
            )

    async def mkdir(self, path: str) -> None:
        """
        Create a directory asynchronously.

        Note: Parent directories are always created automatically by the API.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_async_client()

        try:
            response = await client.make_dir(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "create directory",
                    exists_msg=f"Directory already exists: {path}",
                )
        except (SandboxServiceError, SandboxFileExistsError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e),
                "create directory",
                exists_msg=f"Directory already exists: {path}",
            ) from e

    async def list_dir(self, path: str = ".") -> List[str]:
        """
        List contents of a directory asynchronously.

        Args:
            path: Path to the directory (default: current directory)

        Returns:
            List[str]: Names of files and directories within the specified path.
        """
        client = self._get_async_client()

        try:
            response = await client.list_dir(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "list directory",
                    not_found_msg=f"Directory not found: {path}",
                )
            entries = response.get("entries", [])
            return entries
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "list directory", not_found_msg=f"Directory not found: {path}"
            ) from e

    async def delete_file(self, path: str) -> None:
        """
        Delete a file asynchronously.

        Args:
            path: Absolute path to the file
        """
        client = self._get_async_client()

        try:
            response = await client.delete_file(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "delete file",
                    not_found_msg=f"File not found: {path}",
                )
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "delete file", not_found_msg=f"File not found: {path}"
            ) from e

    async def delete_dir(self, path: str) -> None:
        """
        Delete a directory asynchronously.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_async_client()

        try:
            response = await client.delete_dir(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "delete directory",
                    not_found_msg=f"Directory not found: {path}",
                    not_empty_msg=f"Directory not empty: {path}",
                )
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e),
                "delete directory",
                not_found_msg=f"Directory not found: {path}",
                not_empty_msg=f"Directory not empty: {path}",
            ) from e

    async def rename_file(self, old_path: str, new_path: str) -> None:
        """
        Rename a file asynchronously.

        Args:
            old_path: Current file path
            new_path: New file path
        """
        executor = self._get_async_executor()
        old_path_escaped = escape_shell_arg(old_path)
        new_path_escaped = escape_shell_arg(new_path)
        result = await executor(f"mv {old_path_escaped} {new_path_escaped}")

        if not result.success:
            raise _executor_error(
                result.stderr,
                "rename file",
                not_found_msg=f"File not found: {old_path}",
            )

    async def move_file(self, source_path: str, destination_path: str) -> None:
        """
        Move a file to a different directory asynchronously.

        Args:
            source_path: Current file path
            destination_path: Destination path
        """
        executor = self._get_async_executor()
        source_path_escaped = escape_shell_arg(source_path)
        destination_path_escaped = escape_shell_arg(destination_path)
        result = await executor(f"mv {source_path_escaped} {destination_path_escaped}")

        if not result.success:
            raise _executor_error(
                result.stderr,
                "move file",
                not_found_msg=f"File not found: {source_path}",
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
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)
        result = await executor(f"test -e {path_escaped}")
        return result.success

    async def is_file(self, path: str) -> bool:
        """Check if path is a file asynchronously"""
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)
        result = await executor(f"test -f {path_escaped}")
        return result.success

    async def is_dir(self, path: str) -> bool:
        """Check if path is a directory asynchronously"""
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)
        result = await executor(f"test -d {path_escaped}")
        return result.success

    async def upload_file(
        self,
        local_path: str,
        remote_path: str,
        encoding: str = "utf-8",
        *,
        progress: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        """
        Upload a local file to the sandbox asynchronously.

        On executors v0.0.24+ the file streams from disk through PUT
        /files — binary-safe, constant memory — with optional progress
        callbacks. Older executors keep the legacy JSON behavior (the
        encoding parameter applies there only).

        Args:
            local_path: Path to the local file
            remote_path: Destination path in the sandbox
            encoding: Legacy executors only (default: "utf-8"); the
                streamed routes are binary-safe and ignore it
            progress: Optional callback(done, total), called at most every
                100 ms during the transfer plus a final call

        The transfer is bounded by a 60 s idle timeout only; a per-call
        timeout override parameter is planned with the multipart slice.

        Raises:
            SandboxFileNotFoundError: If local file doesn't exist
        """
        if not os.path.exists(local_path):
            raise SandboxFileNotFoundError(f"Local file not found: {local_path}")

        client = self._get_async_client()
        if await client.has_files_routes():
            reporter = _ProgressReporter(progress, os.path.getsize(local_path))
            with _translating_files_errors("upload file", remote_path):
                digest = _file_sha256(local_path)
                with open(local_path, "rb") as f:
                    reply = await client.files_put(
                        remote_path,
                        _progress_chunks(f, reporter),
                        sha256=digest,
                    )
                if reply["sha256"] != digest:
                    raise SandboxFilesystemError(
                        f"Upload corrupted in transit: executor sha256 "
                        f"{reply['sha256']} != {digest}"
                    )
            return

        with open(local_path, "rb") as f:
            content_bytes = f.read()

        await self.write_file(remote_path, content_bytes, encoding=encoding)

    async def download_file(
        self,
        remote_path: str,
        local_path: str,
        encoding: str = "utf-8",
        *,
        progress: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        """
        Download a file from the sandbox to a local path asynchronously.

        On executors v0.0.24+ the size comes from stat (never a HEAD), the
        bytes stream into <local>.part and rename into place on success:
        a failed download leaves the destination exactly as it was.
        Older executors keep the legacy JSON behavior.

        Args:
            remote_path: Path to the file in the sandbox
            local_path: Destination path on the local filesystem
            encoding: Legacy executors only (default: "utf-8"); the
                streamed routes are binary-safe and ignore it
            progress: Optional callback(done, total), called at most every
                100 ms during the transfer plus a final call

        The transfer is bounded by a 60 s idle timeout only; a per-call
        timeout override parameter is planned with the multipart slice.

        Raises:
            SandboxFileNotFoundError: If remote file doesn't exist
        """
        client = self._get_async_client()
        if await client.has_files_routes():
            part_path = f"{local_path}.part"
            with _translating_files_errors("download file", remote_path):
                entry = await client.files_stat(remote_path)
                reporter = _ProgressReporter(progress, entry["size"])
                done = 0
                renamed = False
                try:
                    with open(part_path, "wb") as out:
                        async for chunk in client.files_read(remote_path):
                            out.write(chunk)
                            done += len(chunk)
                            reporter.update(done)
                    reporter.finish(done)
                    os.replace(part_path, local_path)
                    renamed = True
                finally:
                    if not renamed:
                        try:
                            os.unlink(part_path)
                        except OSError:
                            pass
            return

        file_info = await self.read_file(remote_path, encoding=encoding)

        if isinstance(file_info.content, bytes):
            content_bytes = file_info.content
        else:
            content_bytes = file_info.content.encode(encoding)

        with open(local_path, "wb") as f:
            f.write(content_bytes)

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
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)

        if recursive:
            result = await executor(f"rm -rf {path_escaped}")
        else:
            result = await executor(f"rm {path_escaped}")

        if not result.success:
            raise _executor_error(
                result.stderr, "remove", not_found_msg=f"File not found: {path}"
            )

    def open(
        self, path: str, mode: str = "r", encoding: str = "utf-8"
    ) -> AsyncSandboxFileIO:
        """
        Open a file in the sandbox asynchronously.

        Args:
            path: Path to the file
            mode: Open mode ('r', 'w', 'a', etc.)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.

        Returns:
            AsyncSandboxFileIO: Async file handle
        """
        return AsyncSandboxFileIO(self, path, mode, encoding)


class SandboxFileIO:
    """Synchronous file I/O handle for sandbox files"""

    def __init__(
        self,
        filesystem: SandboxFilesystem,
        path: str,
        mode: str,
        encoding: str = "utf-8",
    ):
        self.filesystem = filesystem
        self.path = path
        self.mode = mode
        self.encoding = encoding
        self._closed = False

    def read(self) -> Union[str, bytes]:
        """Read file content synchronously"""
        if "r" not in self.mode:
            raise ValueError("File not opened for reading")

        if self._closed:
            raise ValueError("File is closed")

        file_info = self.filesystem.read_file(self.path, encoding=self.encoding)
        return file_info.content

    def write(self, content: Union[str, bytes]) -> None:
        """Write content to file synchronously"""
        if "w" not in self.mode and "a" not in self.mode:
            raise ValueError("File not opened for writing")

        if self._closed:
            raise ValueError("File is closed")

        if "a" in self.mode:
            try:
                existing = self.filesystem.read_file(self.path, encoding=self.encoding)
                if isinstance(existing.content, bytes) and isinstance(content, bytes):
                    content = existing.content + content
                elif isinstance(existing.content, str) and isinstance(content, str):
                    content = existing.content + content
                else:
                    raise TypeError("Cannot mix bytes and str content in append mode")
            except SandboxFileNotFoundError:
                pass

        self.filesystem.write_file(self.path, content, encoding=self.encoding)

    def close(self) -> None:
        """Close the file"""
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncSandboxFileIO:
    """Async file I/O handle for sandbox files"""

    def __init__(
        self,
        filesystem: AsyncSandboxFilesystem,
        path: str,
        mode: str,
        encoding: str = "utf-8",
    ):
        self.filesystem = filesystem
        self.path = path
        self.mode = mode
        self.encoding = encoding
        self._closed = False

    async def read(self) -> Union[str, bytes]:
        """Read file content asynchronously"""
        if "r" not in self.mode:
            raise ValueError("File not opened for reading")

        if self._closed:
            raise ValueError("File is closed")

        file_info = await self.filesystem.read_file(self.path, encoding=self.encoding)
        return file_info.content

    async def write(self, content: Union[str, bytes]) -> None:
        """Write content to file asynchronously"""
        if "w" not in self.mode and "a" not in self.mode:
            raise ValueError("File not opened for writing")

        if self._closed:
            raise ValueError("File is closed")

        if "a" in self.mode:
            try:
                existing = await self.filesystem.read_file(
                    self.path, encoding=self.encoding
                )
                if isinstance(existing.content, bytes) and isinstance(content, bytes):
                    content = existing.content + content
                elif isinstance(existing.content, str) and isinstance(content, str):
                    content = existing.content + content
                else:
                    raise TypeError("Cannot mix bytes and str content in append mode")
            except SandboxFileNotFoundError:
                pass

        await self.filesystem.write_file(self.path, content, encoding=self.encoding)

    def close(self) -> None:
        """Close the file"""
        self._closed = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
