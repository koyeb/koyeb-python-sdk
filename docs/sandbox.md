<a id="koyeb/sandbox"></a>

# koyeb/sandbox

Koyeb Sandbox - Interactive execution environment for running arbitrary code on Koyeb

<a id="koyeb/sandbox.exec"></a>

# koyeb/sandbox.exec

Command execution utilities for Koyeb Sandbox instances
Using SandboxClient HTTP API

<a id="koyeb/sandbox.exec.CommandStatus"></a>

## CommandStatus Objects

```python
class CommandStatus(str, Enum)
```

Command execution status

<a id="koyeb/sandbox.exec.CommandResult"></a>

## CommandResult Objects

```python
@dataclass
class CommandResult()
```

Result of a command execution using Koyeb API models

<a id="koyeb/sandbox.exec.CommandResult.success"></a>

#### success

```python
@property
def success() -> bool
```

Check if command executed successfully

<a id="koyeb/sandbox.exec.CommandResult.output"></a>

#### output

```python
@property
def output() -> str
```

Get combined stdout and stderr output

<a id="koyeb/sandbox.exec.SandboxCommandError"></a>

## SandboxCommandError Objects

```python
class SandboxCommandError(SandboxError)
```

Raised when command execution fails

<a id="koyeb/sandbox.exec.SandboxExecutor"></a>

## SandboxExecutor Objects

```python
class SandboxExecutor()
```

Synchronous command execution interface for Koyeb Sandbox instances.
Bound to a specific sandbox instance.

For async usage, use AsyncSandboxExecutor instead.

<a id="koyeb/sandbox.exec.SandboxExecutor.__call__"></a>

#### \_\_call\_\_

```python
def __call__(
        command: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        on_stdout: Optional[Callable[[str], None]] = None,
        on_stderr: Optional[Callable[[str], None]] = None) -> CommandResult
```

Execute a command in a shell synchronously. Supports streaming output via callbacks.

**Arguments**:

- `command` - Command to execute as a string (e.g., "python -c 'print(2+2)'")
- `cwd` - Working directory for the command
- `env` - Environment variables for the command
- `timeout` - Command timeout in seconds (enforced for HTTP requests)
- `on_stdout` - Optional callback for streaming stdout chunks
- `on_stderr` - Optional callback for streaming stderr chunks
  

**Returns**:

- `CommandResult` - Result of the command execution
  

**Example**:

    ```python
    # Synchronous execution
    result = sandbox.exec("echo hello")

    # With streaming callbacks
    result = sandbox.exec(
        "echo hello; sleep 1; echo world",
        on_stdout=lambda data: print(f"OUT: {data}"),
        on_stderr=lambda data: print(f"ERR: {data}"),
    )
    ```

<a id="koyeb/sandbox.exec.AsyncSandboxExecutor"></a>

## AsyncSandboxExecutor Objects

```python
class AsyncSandboxExecutor(SandboxExecutor)
```

Async command execution interface for Koyeb Sandbox instances.
Bound to a specific sandbox instance.

Inherits from SandboxExecutor and provides async command execution.

<a id="koyeb/sandbox.exec.AsyncSandboxExecutor.__call__"></a>

#### \_\_call\_\_

```python
async def __call__(
        command: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        on_stdout: Optional[Callable[[str], None]] = None,
        on_stderr: Optional[Callable[[str], None]] = None) -> CommandResult
```

Execute a command in a shell asynchronously. Supports streaming output via callbacks.

**Arguments**:

- `command` - Command to execute as a string (e.g., "python -c 'print(2+2)'")
- `cwd` - Working directory for the command
- `env` - Environment variables for the command
- `timeout` - Command timeout in seconds (enforced for HTTP requests)
- `on_stdout` - Optional callback for streaming stdout chunks
- `on_stderr` - Optional callback for streaming stderr chunks
  

**Returns**:

- `CommandResult` - Result of the command execution
  

**Example**:

    ```python
    # Async execution
    result = await sandbox.exec("echo hello")

    # With streaming callbacks
    result = await sandbox.exec(
        "echo hello; sleep 1; echo world",
        on_stdout=lambda data: print(f"OUT: {data}"),
        on_stderr=lambda data: print(f"ERR: {data}"),
    )
    ```

<a id="koyeb/sandbox.filesystem"></a>

# koyeb/sandbox.filesystem

Filesystem operations for Koyeb Sandbox instances
Using SandboxClient HTTP API

<a id="koyeb/sandbox.filesystem.SandboxFilesystemError"></a>

## SandboxFilesystemError Objects

```python
class SandboxFilesystemError(SandboxError)
```

Base exception for filesystem operations

<a id="koyeb/sandbox.filesystem.SandboxFileNotFoundError"></a>

## SandboxFileNotFoundError Objects

```python
class SandboxFileNotFoundError(SandboxFilesystemError)
```

Raised when file or directory not found

<a id="koyeb/sandbox.filesystem.SandboxFileExistsError"></a>

## SandboxFileExistsError Objects

```python
class SandboxFileExistsError(SandboxFilesystemError)
```

Raised when file already exists

<a id="koyeb/sandbox.filesystem.FileInfo"></a>

## FileInfo Objects

```python
@dataclass
class FileInfo()
```

File information

<a id="koyeb/sandbox.filesystem.SandboxFilesystem"></a>

## SandboxFilesystem Objects

```python
class SandboxFilesystem()
```

Synchronous filesystem operations for Koyeb Sandbox instances.
Using SandboxClient HTTP API.

For async usage, use AsyncSandboxFilesystem instead.

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.write_file"></a>

#### write\_file

```python
def write_file(path: str,
               content: Union[str, bytes],
               encoding: str = "utf-8") -> None
```

Write content to a file synchronously.

**Arguments**:

- `path` - Absolute path to the file
- `content` - Content to write (string or bytes)
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary data.

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.read_file"></a>

#### read\_file

```python
def read_file(path: str, encoding: str = "utf-8") -> FileInfo
```

Read a file from the sandbox synchronously.

**Arguments**:

- `path` - Absolute path to the file
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary data.
  

**Returns**:

- `FileInfo` - Object with content and encoding

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.mkdir"></a>

#### mkdir

```python
def mkdir(path: str, recursive: bool = False) -> None
```

Create a directory synchronously.

**Arguments**:

- `path` - Absolute path to the directory
- `recursive` - Create parent directories if needed (default: False, not used - API always creates parents)

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.list_dir"></a>

#### list\_dir

```python
def list_dir(path: str = ".") -> List[str]
```

List contents of a directory synchronously.

**Arguments**:

- `path` - Path to the directory (default: current directory)
  

**Returns**:

- `List[str]` - Names of files and directories within the specified path.

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.delete_file"></a>

#### delete\_file

```python
def delete_file(path: str) -> None
```

Delete a file synchronously.

**Arguments**:

- `path` - Absolute path to the file

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.delete_dir"></a>

#### delete\_dir

```python
def delete_dir(path: str) -> None
```

Delete a directory synchronously.

**Arguments**:

- `path` - Absolute path to the directory

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.rename_file"></a>

#### rename\_file

```python
def rename_file(old_path: str, new_path: str) -> None
```

Rename a file synchronously.

**Arguments**:

- `old_path` - Current file path
- `new_path` - New file path

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.move_file"></a>

#### move\_file

```python
def move_file(source_path: str, destination_path: str) -> None
```

Move a file to a different directory synchronously.

**Arguments**:

- `source_path` - Current file path
- `destination_path` - Destination path

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.write_files"></a>

#### write\_files

```python
def write_files(files: List[Dict[str, str]]) -> None
```

Write multiple files in a single operation synchronously.

**Arguments**:

- `files` - List of dictionaries, each with 'path', 'content', and optional 'encoding'.

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.exists"></a>

#### exists

```python
def exists(path: str) -> bool
```

Check if file/directory exists synchronously

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.is_file"></a>

#### is\_file

```python
def is_file(path: str) -> bool
```

Check if path is a file synchronously

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.is_dir"></a>

#### is\_dir

```python
def is_dir(path: str) -> bool
```

Check if path is a directory synchronously

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.upload_file"></a>

#### upload\_file

```python
def upload_file(local_path: str,
                remote_path: str,
                encoding: str = "utf-8") -> None
```

Upload a local file to the sandbox synchronously.

**Arguments**:

- `local_path` - Path to the local file
- `remote_path` - Destination path in the sandbox
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary files.
  

**Raises**:

- `SandboxFileNotFoundError` - If local file doesn't exist
- `UnicodeDecodeError` - If file cannot be decoded with specified encoding

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.download_file"></a>

#### download\_file

```python
def download_file(remote_path: str,
                  local_path: str,
                  encoding: str = "utf-8") -> None
```

Download a file from the sandbox to a local path synchronously.

**Arguments**:

- `remote_path` - Path to the file in the sandbox
- `local_path` - Destination path on the local filesystem
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary files.
  

**Raises**:

- `SandboxFileNotFoundError` - If remote file doesn't exist

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.ls"></a>

#### ls

```python
def ls(path: str = ".") -> List[str]
```

List directory contents synchronously.

**Arguments**:

- `path` - Path to list
  

**Returns**:

  List of file/directory names

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.rm"></a>

#### rm

```python
def rm(path: str, recursive: bool = False) -> None
```

Remove file or directory synchronously.

**Arguments**:

- `path` - Path to remove
- `recursive` - Remove recursively

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.open"></a>

#### open

```python
def open(path: str, mode: str = "r") -> SandboxFileIO
```

Open a file in the sandbox synchronously.

**Arguments**:

- `path` - Path to the file
- `mode` - Open mode ('r', 'w', 'a', etc.)
  

**Returns**:

- `SandboxFileIO` - File handle

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem"></a>

## AsyncSandboxFilesystem Objects

```python
class AsyncSandboxFilesystem(SandboxFilesystem)
```

Async filesystem operations for Koyeb Sandbox instances.
Inherits from SandboxFilesystem and provides async methods.

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.write_file"></a>

#### write\_file

```python
@async_wrapper("write_file")
async def write_file(path: str,
                     content: Union[str, bytes],
                     encoding: str = "utf-8") -> None
```

Write content to a file asynchronously.

**Arguments**:

- `path` - Absolute path to the file
- `content` - Content to write (string or bytes)
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary data.

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.read_file"></a>

#### read\_file

```python
@async_wrapper("read_file")
async def read_file(path: str, encoding: str = "utf-8") -> FileInfo
```

Read a file from the sandbox asynchronously.

**Arguments**:

- `path` - Absolute path to the file
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary data.
  

**Returns**:

- `FileInfo` - Object with content and encoding

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.mkdir"></a>

#### mkdir

```python
@async_wrapper("mkdir")
async def mkdir(path: str, recursive: bool = False) -> None
```

Create a directory asynchronously.

**Arguments**:

- `path` - Absolute path to the directory
- `recursive` - Create parent directories if needed (default: False, not used - API always creates parents)

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.list_dir"></a>

#### list\_dir

```python
@async_wrapper("list_dir")
async def list_dir(path: str = ".") -> List[str]
```

List contents of a directory asynchronously.

**Arguments**:

- `path` - Path to the directory (default: current directory)
  

**Returns**:

- `List[str]` - Names of files and directories within the specified path.

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.delete_file"></a>

#### delete\_file

```python
@async_wrapper("delete_file")
async def delete_file(path: str) -> None
```

Delete a file asynchronously.

**Arguments**:

- `path` - Absolute path to the file

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.delete_dir"></a>

#### delete\_dir

```python
@async_wrapper("delete_dir")
async def delete_dir(path: str) -> None
```

Delete a directory asynchronously.

**Arguments**:

- `path` - Absolute path to the directory

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.rename_file"></a>

#### rename\_file

```python
@async_wrapper("rename_file")
async def rename_file(old_path: str, new_path: str) -> None
```

Rename a file asynchronously.

**Arguments**:

- `old_path` - Current file path
- `new_path` - New file path

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.move_file"></a>

#### move\_file

```python
@async_wrapper("move_file")
async def move_file(source_path: str, destination_path: str) -> None
```

Move a file to a different directory asynchronously.

**Arguments**:

- `source_path` - Current file path
- `destination_path` - Destination path

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.write_files"></a>

#### write\_files

```python
async def write_files(files: List[Dict[str, str]]) -> None
```

Write multiple files in a single operation asynchronously.

**Arguments**:

- `files` - List of dictionaries, each with 'path', 'content', and optional 'encoding'.

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.exists"></a>

#### exists

```python
@async_wrapper("exists")
async def exists(path: str) -> bool
```

Check if file/directory exists asynchronously

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.is_file"></a>

#### is\_file

```python
@async_wrapper("is_file")
async def is_file(path: str) -> bool
```

Check if path is a file asynchronously

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.is_dir"></a>

#### is\_dir

```python
@async_wrapper("is_dir")
async def is_dir(path: str) -> bool
```

Check if path is a directory asynchronously

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.upload_file"></a>

#### upload\_file

```python
@async_wrapper("upload_file")
async def upload_file(local_path: str,
                      remote_path: str,
                      encoding: str = "utf-8") -> None
```

Upload a local file to the sandbox asynchronously.

**Arguments**:

- `local_path` - Path to the local file
- `remote_path` - Destination path in the sandbox
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary files.

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.download_file"></a>

#### download\_file

```python
@async_wrapper("download_file")
async def download_file(remote_path: str,
                        local_path: str,
                        encoding: str = "utf-8") -> None
```

Download a file from the sandbox to a local path asynchronously.

**Arguments**:

- `remote_path` - Path to the file in the sandbox
- `local_path` - Destination path on the local filesystem
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary files.

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.ls"></a>

#### ls

```python
async def ls(path: str = ".") -> List[str]
```

List directory contents asynchronously.

**Arguments**:

- `path` - Path to list
  

**Returns**:

  List of file/directory names

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.rm"></a>

#### rm

```python
@async_wrapper("rm")
async def rm(path: str, recursive: bool = False) -> None
```

Remove file or directory asynchronously.

**Arguments**:

- `path` - Path to remove
- `recursive` - Remove recursively

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.open"></a>

#### open

```python
def open(path: str, mode: str = "r") -> AsyncSandboxFileIO
```

Open a file in the sandbox asynchronously.

**Arguments**:

- `path` - Path to the file
- `mode` - Open mode ('r', 'w', 'a', etc.)
  

**Returns**:

- `AsyncSandboxFileIO` - Async file handle

<a id="koyeb/sandbox.filesystem.SandboxFileIO"></a>

## SandboxFileIO Objects

```python
class SandboxFileIO()
```

Synchronous file I/O handle for sandbox files

<a id="koyeb/sandbox.filesystem.SandboxFileIO.read"></a>

#### read

```python
def read() -> str
```

Read file content synchronously

<a id="koyeb/sandbox.filesystem.SandboxFileIO.write"></a>

#### write

```python
def write(content: str) -> None
```

Write content to file synchronously

<a id="koyeb/sandbox.filesystem.SandboxFileIO.close"></a>

#### close

```python
def close() -> None
```

Close the file

<a id="koyeb/sandbox.filesystem.AsyncSandboxFileIO"></a>

## AsyncSandboxFileIO Objects

```python
class AsyncSandboxFileIO()
```

Async file I/O handle for sandbox files

<a id="koyeb/sandbox.filesystem.AsyncSandboxFileIO.read"></a>

#### read

```python
async def read() -> str
```

Read file content asynchronously

<a id="koyeb/sandbox.filesystem.AsyncSandboxFileIO.write"></a>

#### write

```python
async def write(content: str) -> None
```

Write content to file asynchronously

<a id="koyeb/sandbox.filesystem.AsyncSandboxFileIO.close"></a>

#### close

```python
def close() -> None
```

Close the file

<a id="koyeb/sandbox.sandbox"></a>

# koyeb/sandbox.sandbox

Koyeb Sandbox - Python SDK for creating and managing Koyeb sandboxes

<a id="koyeb/sandbox.sandbox.ProcessInfo"></a>

## ProcessInfo Objects

```python
@dataclass
class ProcessInfo()
```

Type definition for process information returned by list_processes.

<a id="koyeb/sandbox.sandbox.ProcessInfo.id"></a>

#### id

Process ID (UUID string)

<a id="koyeb/sandbox.sandbox.ProcessInfo.command"></a>

#### command

The command that was executed

<a id="koyeb/sandbox.sandbox.ProcessInfo.status"></a>

#### status

Process status (e.g., "running", "completed")

<a id="koyeb/sandbox.sandbox.ProcessInfo.pid"></a>

#### pid

OS process ID (if running)

<a id="koyeb/sandbox.sandbox.ProcessInfo.exit_code"></a>

#### exit\_code

Exit code (if completed)

<a id="koyeb/sandbox.sandbox.ProcessInfo.started_at"></a>

#### started\_at

ISO 8601 timestamp when process started

<a id="koyeb/sandbox.sandbox.ExposedPort"></a>

## ExposedPort Objects

```python
@dataclass
class ExposedPort()
```

Result of exposing a port via TCP proxy.

<a id="koyeb/sandbox.sandbox.Sandbox"></a>

## Sandbox Objects

```python
class Sandbox()
```

Synchronous sandbox for running code on Koyeb infrastructure.
Provides creation and deletion functionality with proper health polling.

<a id="koyeb/sandbox.sandbox.Sandbox.id"></a>

#### id

```python
@property
def id() -> str
```

Get the service ID of the sandbox.

<a id="koyeb/sandbox.sandbox.Sandbox.create"></a>

#### create

```python
@classmethod
def create(cls,
           image: str = "koyeb/sandbox",
           name: str = "quick-sandbox",
           wait_ready: bool = True,
           instance_type: str = "micro",
           exposed_port_protocol: Optional[str] = None,
           env: Optional[Dict[str, str]] = None,
           region: Optional[str] = None,
           api_token: Optional[str] = None,
           timeout: int = 300,
           idle_timeout: Optional[IdleTimeout] = None,
           enable_tcp_proxy: bool = False,
           privileged: bool = False) -> Sandbox
```

Create a new sandbox instance.

**Arguments**:

- `image` - Docker image to use (default: koyeb/sandbox)
- `name` - Name of the sandbox
- `wait_ready` - Wait for sandbox to be ready (default: True)
- `instance_type` - Instance type (default: nano)
- `exposed_port_protocol` - Protocol to expose ports with ("http" or "http2").
  If None, defaults to "http".
  If provided, must be one of "http" or "http2".
- `env` - Environment variables
- `region` - Region to deploy to (default: "na")
- `api_token` - Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
- `timeout` - Timeout for sandbox creation in seconds
- `idle_timeout` - Idle timeout configuration for scale-to-zero
  - None: Auto-enable (light_sleep=300s, deep_sleep=600s)
  - 0: Disable scale-to-zero (keep always-on)
  - int > 0: Deep sleep only (e.g., 600 for 600s deep sleep)
  - dict: Explicit configuration with {"light_sleep": 300, "deep_sleep": 600}
- `enable_tcp_proxy` - If True, enables TCP proxy for direct TCP access to port 3031
- `privileged` - If True, run the container in privileged mode (default: False)
  

**Returns**:

- `Sandbox` - A new Sandbox instance
  

**Raises**:

- `ValueError` - If API token is not provided
- `SandboxTimeoutError` - If wait_ready is True and sandbox does not become ready within timeout

<a id="koyeb/sandbox.sandbox.Sandbox.get_from_id"></a>

#### get\_from\_id

```python
@classmethod
def get_from_id(cls, id: str, api_token: Optional[str] = None) -> "Sandbox"
```

Get a sandbox by service ID.

**Arguments**:

- `id` - Service ID of the sandbox
- `api_token` - Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
  

**Returns**:

- `Sandbox` - The Sandbox instance
  

**Raises**:

- `ValueError` - If API token is not provided or id is invalid
- `SandboxError` - If sandbox is not found or retrieval fails

<a id="koyeb/sandbox.sandbox.Sandbox.wait_ready"></a>

#### wait\_ready

```python
def wait_ready(timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
               poll_interval: float = DEFAULT_POLL_INTERVAL) -> bool
```

Wait for sandbox to become ready with proper polling.

**Arguments**:

- `timeout` - Maximum time to wait in seconds
- `poll_interval` - Time between health checks in seconds
  

**Returns**:

- `bool` - True if sandbox became ready, False if timeout

<a id="koyeb/sandbox.sandbox.Sandbox.wait_tcp_proxy_ready"></a>

#### wait\_tcp\_proxy\_ready

```python
def wait_tcp_proxy_ready(timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
                         poll_interval: float = DEFAULT_POLL_INTERVAL) -> bool
```

Wait for TCP proxy to become ready and available.

Polls the deployment metadata until the TCP proxy information is available.
This is useful when enable_tcp_proxy=True was set during sandbox creation,
as the proxy information may not be immediately available.

**Arguments**:

- `timeout` - Maximum time to wait in seconds
- `poll_interval` - Time between checks in seconds
  

**Returns**:

- `bool` - True if TCP proxy became ready, False if timeout

<a id="koyeb/sandbox.sandbox.Sandbox.delete"></a>

#### delete

```python
def delete() -> None
```

Delete the sandbox instance.

<a id="koyeb/sandbox.sandbox.Sandbox.get_domain"></a>

#### get\_domain

```python
def get_domain() -> Optional[str]
```

Get the public domain of the sandbox.

Returns the domain name (e.g., "app-name-org.koyeb.app") without protocol or path.
To construct the URL, use: f"https://{sandbox.get_domain()}"

**Returns**:

- `Optional[str]` - The domain name or None if unavailable

<a id="koyeb/sandbox.sandbox.Sandbox.get_tcp_proxy_info"></a>

#### get\_tcp\_proxy\_info

```python
def get_tcp_proxy_info() -> Optional[tuple[str, int]]
```

Get the TCP proxy host and port for the sandbox.

Returns the TCP proxy host and port as a tuple (host, port) for direct TCP access to port 3031.
This is only available if enable_tcp_proxy=True was set when creating the sandbox.

**Returns**:

  Optional[tuple[str, int]]: A tuple of (host, port) or None if unavailable

<a id="koyeb/sandbox.sandbox.Sandbox.is_healthy"></a>

#### is\_healthy

```python
def is_healthy() -> bool
```

Check if sandbox is healthy and ready for operations

<a id="koyeb/sandbox.sandbox.Sandbox.filesystem"></a>

#### filesystem

```python
@property
def filesystem() -> "SandboxFilesystem"
```

Get filesystem operations interface

<a id="koyeb/sandbox.sandbox.Sandbox.exec"></a>

#### exec

```python
@property
def exec() -> "SandboxExecutor"
```

Get command execution interface

<a id="koyeb/sandbox.sandbox.Sandbox.expose_port"></a>

#### expose\_port

```python
def expose_port(port: int) -> ExposedPort
```

Expose a port to external connections via TCP proxy.

Binds the specified internal port to the TCP proxy, allowing external
connections to reach services running on that port inside the sandbox.
Automatically unbinds any existing port before binding the new one.

**Arguments**:

- `port` - The internal port number to expose (must be a valid port number between 1 and 65535)
  

**Returns**:

- `ExposedPort` - An object with `port` and `exposed_at` attributes:
  - port: The exposed port number
  - exposed_at: The full URL with https:// protocol (e.g., "https://app-name-org.koyeb.app")
  

**Raises**:

- `ValueError` - If port is not in valid range [1, 65535]
- `SandboxError` - If the port binding operation fails
  

**Notes**:

  - Only one port can be exposed at a time
  - Any existing port binding is automatically unbound before binding the new port
  - The port must be available and accessible within the sandbox environment
  - The TCP proxy is accessed via get_tcp_proxy_info() which returns (host, port)
  

**Example**:

  >>> result = sandbox.expose_port(8080)
  >>> result.port
  8080
  >>> result.exposed_at
  'https://app-name-org.koyeb.app'

<a id="koyeb/sandbox.sandbox.Sandbox.unexpose_port"></a>

#### unexpose\_port

```python
def unexpose_port() -> None
```

Unexpose a port from external connections.

Removes the TCP proxy port binding, stopping traffic forwarding to the
previously bound port.

**Raises**:

- `SandboxError` - If the port unbinding operation fails
  

**Notes**:

  - After unexposing, the TCP proxy will no longer forward traffic
  - Safe to call even if no port is currently bound

<a id="koyeb/sandbox.sandbox.Sandbox.launch_process"></a>

#### launch\_process

```python
def launch_process(cmd: str,
                   cwd: Optional[str] = None,
                   env: Optional[Dict[str, str]] = None) -> str
```

Launch a background process in the sandbox.

Starts a long-running background process that continues executing even after
the method returns. Use this for servers, workers, or other long-running tasks.

**Arguments**:

- `cmd` - The shell command to execute as a background process
- `cwd` - Optional working directory for the process
- `env` - Optional environment variables to set/override for the process
  

**Returns**:

- `str` - The unique process ID (UUID string) that can be used to manage the process
  

**Raises**:

- `SandboxError` - If the process launch fails
  

**Example**:

  >>> process_id = sandbox.launch_process("python -u server.py")
  >>> print(f"Started process: {process_id}")

<a id="koyeb/sandbox.sandbox.Sandbox.kill_process"></a>

#### kill\_process

```python
def kill_process(process_id: str) -> None
```

Kill a background process by its ID.

Terminates a running background process. This sends a SIGTERM signal to the process,
allowing it to clean up gracefully. If the process doesn't terminate within a timeout,
it will be forcefully killed with SIGKILL.

**Arguments**:

- `process_id` - The unique process ID (UUID string) to kill
  

**Raises**:

- `SandboxError` - If the process kill operation fails
  

**Example**:

  >>> sandbox.kill_process("550e8400-e29b-41d4-a716-446655440000")

<a id="koyeb/sandbox.sandbox.Sandbox.list_processes"></a>

#### list\_processes

```python
def list_processes() -> List[ProcessInfo]
```

List all background processes.

Returns information about all currently running and recently completed background
processes. This includes both active processes and processes that have completed
(which remain in memory until server restart).

**Returns**:

- `List[ProcessInfo]` - List of process objects, each containing:
  - id: Process ID (UUID string)
  - command: The command that was executed
  - status: Process status (e.g., "running", "completed")
  - pid: OS process ID (if running)
  - exit_code: Exit code (if completed)
  - started_at: ISO 8601 timestamp when process started
  - completed_at: ISO 8601 timestamp when process completed (if applicable)
  

**Raises**:

- `SandboxError` - If listing processes fails
  

**Example**:

  >>> processes = sandbox.list_processes()
  >>> for process in processes:
  ...     print(f"{process.id}: {process.command} - {process.status}")

<a id="koyeb/sandbox.sandbox.Sandbox.kill_all_processes"></a>

#### kill\_all\_processes

```python
def kill_all_processes() -> int
```

Kill all running background processes.

Convenience method that lists all processes and kills them all. This is useful
for cleanup operations.

**Returns**:

- `int` - The number of processes that were killed
  

**Raises**:

- `SandboxError` - If listing or killing processes fails
  

**Example**:

  >>> count = sandbox.kill_all_processes()
  >>> print(f"Killed {count} processes")

<a id="koyeb/sandbox.sandbox.Sandbox.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__() -> "Sandbox"
```

Context manager entry - returns self.

<a id="koyeb/sandbox.sandbox.Sandbox.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(exc_type, exc_val, exc_tb) -> None
```

Context manager exit - automatically deletes the sandbox.

<a id="koyeb/sandbox.sandbox.AsyncSandbox"></a>

## AsyncSandbox Objects

```python
class AsyncSandbox(Sandbox)
```

Async sandbox for running code on Koyeb infrastructure.
Inherits from Sandbox and provides async wrappers for all operations.

<a id="koyeb/sandbox.sandbox.AsyncSandbox.get_from_id"></a>

#### get\_from\_id

```python
@classmethod
async def get_from_id(cls,
                      id: str,
                      api_token: Optional[str] = None) -> "AsyncSandbox"
```

Get a sandbox by service ID asynchronously.

**Arguments**:

- `id` - Service ID of the sandbox
- `api_token` - Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
  

**Returns**:

- `AsyncSandbox` - The AsyncSandbox instance
  

**Raises**:

- `ValueError` - If API token is not provided or id is invalid
- `SandboxError` - If sandbox is not found or retrieval fails

<a id="koyeb/sandbox.sandbox.AsyncSandbox.create"></a>

#### create

```python
@classmethod
async def create(cls,
                 image: str = "koyeb/sandbox",
                 name: str = "quick-sandbox",
                 wait_ready: bool = True,
                 instance_type: str = "nano",
                 exposed_port_protocol: Optional[str] = None,
                 env: Optional[Dict[str, str]] = None,
                 region: Optional[str] = None,
                 api_token: Optional[str] = None,
                 timeout: int = 300,
                 idle_timeout: Optional[IdleTimeout] = None,
                 enable_tcp_proxy: bool = False,
                 privileged: bool = False) -> AsyncSandbox
```

Create a new sandbox instance with async support.

**Arguments**:

- `image` - Docker image to use (default: koyeb/sandbox)
- `name` - Name of the sandbox
- `wait_ready` - Wait for sandbox to be ready (default: True)
- `instance_type` - Instance type (default: nano)
- `exposed_port_protocol` - Protocol to expose ports with ("http" or "http2").
  If None, defaults to "http".
  If provided, must be one of "http" or "http2".
- `env` - Environment variables
- `region` - Region to deploy to (default: "na")
- `api_token` - Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
- `timeout` - Timeout for sandbox creation in seconds
- `idle_timeout` - Idle timeout configuration for scale-to-zero
  - None: Auto-enable (light_sleep=300s, deep_sleep=600s)
  - 0: Disable scale-to-zero (keep always-on)
  - int > 0: Deep sleep only (e.g., 600 for 600s deep sleep)
  - dict: Explicit configuration with {"light_sleep": 300, "deep_sleep": 600}
- `enable_tcp_proxy` - If True, enables TCP proxy for direct TCP access to port 3031
- `privileged` - If True, run the container in privileged mode (default: False)
  

**Returns**:

- `AsyncSandbox` - A new AsyncSandbox instance
  

**Raises**:

- `ValueError` - If API token is not provided
- `SandboxTimeoutError` - If wait_ready is True and sandbox does not become ready within timeout

<a id="koyeb/sandbox.sandbox.AsyncSandbox.wait_ready"></a>

#### wait\_ready

```python
async def wait_ready(timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
                     poll_interval: float = DEFAULT_POLL_INTERVAL) -> bool
```

Wait for sandbox to become ready with proper async polling.

**Arguments**:

- `timeout` - Maximum time to wait in seconds
- `poll_interval` - Time between health checks in seconds
  

**Returns**:

- `bool` - True if sandbox became ready, False if timeout

<a id="koyeb/sandbox.sandbox.AsyncSandbox.wait_tcp_proxy_ready"></a>

#### wait\_tcp\_proxy\_ready

```python
async def wait_tcp_proxy_ready(
        timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
        poll_interval: float = DEFAULT_POLL_INTERVAL) -> bool
```

Wait for TCP proxy to become ready and available asynchronously.

Polls the deployment metadata until the TCP proxy information is available.
This is useful when enable_tcp_proxy=True was set during sandbox creation,
as the proxy information may not be immediately available.

**Arguments**:

- `timeout` - Maximum time to wait in seconds
- `poll_interval` - Time between checks in seconds
  

**Returns**:

- `bool` - True if TCP proxy became ready, False if timeout

<a id="koyeb/sandbox.sandbox.AsyncSandbox.delete"></a>

#### delete

```python
@async_wrapper("delete")
async def delete() -> None
```

Delete the sandbox instance asynchronously.

<a id="koyeb/sandbox.sandbox.AsyncSandbox.is_healthy"></a>

#### is\_healthy

```python
@async_wrapper("is_healthy")
async def is_healthy() -> bool
```

Check if sandbox is healthy and ready for operations asynchronously

<a id="koyeb/sandbox.sandbox.AsyncSandbox.exec"></a>

#### exec

```python
@property
def exec() -> "AsyncSandboxExecutor"
```

Get async command execution interface

<a id="koyeb/sandbox.sandbox.AsyncSandbox.filesystem"></a>

#### filesystem

```python
@property
def filesystem() -> "AsyncSandboxFilesystem"
```

Get filesystem operations interface

<a id="koyeb/sandbox.sandbox.AsyncSandbox.expose_port"></a>

#### expose\_port

```python
@async_wrapper("expose_port")
async def expose_port(port: int) -> ExposedPort
```

Expose a port to external connections via TCP proxy asynchronously.

<a id="koyeb/sandbox.sandbox.AsyncSandbox.unexpose_port"></a>

#### unexpose\_port

```python
@async_wrapper("unexpose_port")
async def unexpose_port() -> None
```

Unexpose a port from external connections asynchronously.

<a id="koyeb/sandbox.sandbox.AsyncSandbox.launch_process"></a>

#### launch\_process

```python
@async_wrapper("launch_process")
async def launch_process(cmd: str,
                         cwd: Optional[str] = None,
                         env: Optional[Dict[str, str]] = None) -> str
```

Launch a background process in the sandbox asynchronously.

<a id="koyeb/sandbox.sandbox.AsyncSandbox.kill_process"></a>

#### kill\_process

```python
@async_wrapper("kill_process")
async def kill_process(process_id: str) -> None
```

Kill a background process by its ID asynchronously.

<a id="koyeb/sandbox.sandbox.AsyncSandbox.list_processes"></a>

#### list\_processes

```python
@async_wrapper("list_processes")
async def list_processes() -> List[ProcessInfo]
```

List all background processes asynchronously.

<a id="koyeb/sandbox.sandbox.AsyncSandbox.kill_all_processes"></a>

#### kill\_all\_processes

```python
async def kill_all_processes() -> int
```

Kill all running background processes asynchronously.

<a id="koyeb/sandbox.sandbox.AsyncSandbox.__aenter__"></a>

#### \_\_aenter\_\_

```python
async def __aenter__() -> "AsyncSandbox"
```

Async context manager entry - returns self.

<a id="koyeb/sandbox.sandbox.AsyncSandbox.__aexit__"></a>

#### \_\_aexit\_\_

```python
async def __aexit__(exc_type, exc_val, exc_tb) -> None
```

Async context manager exit - automatically deletes the sandbox.

<a id="koyeb/sandbox.utils"></a>

# koyeb/sandbox.utils

Utility functions for Koyeb Sandbox

<a id="koyeb/sandbox.utils.DEFAULT_INSTANCE_WAIT_TIMEOUT"></a>

#### DEFAULT\_INSTANCE\_WAIT\_TIMEOUT

seconds

<a id="koyeb/sandbox.utils.DEFAULT_POLL_INTERVAL"></a>

#### DEFAULT\_POLL\_INTERVAL

seconds

<a id="koyeb/sandbox.utils.DEFAULT_COMMAND_TIMEOUT"></a>

#### DEFAULT\_COMMAND\_TIMEOUT

seconds

<a id="koyeb/sandbox.utils.DEFAULT_HTTP_TIMEOUT"></a>

#### DEFAULT\_HTTP\_TIMEOUT

seconds for HTTP requests

<a id="koyeb/sandbox.utils.IdleTimeoutConfig"></a>

## IdleTimeoutConfig Objects

```python
class IdleTimeoutConfig(TypedDict)
```

Configuration for idle timeout with light and deep sleep.

<a id="koyeb/sandbox.utils.IdleTimeoutConfig.light_sleep"></a>

#### light\_sleep

Optional, but if provided, deep_sleep is required

<a id="koyeb/sandbox.utils.IdleTimeoutConfig.deep_sleep"></a>

#### deep\_sleep

Required

<a id="koyeb/sandbox.utils.get_api_client"></a>

#### get\_api\_client

```python
def get_api_client(
    api_token: Optional[str] = None,
    host: Optional[str] = None
) -> tuple[AppsApi, ServicesApi, InstancesApi, CatalogInstancesApi]
```

Get configured API clients for Koyeb operations.

**Arguments**:

- `api_token` - Koyeb API token. If not provided, will try to get from KOYEB_API_TOKEN env var
- `host` - Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)
  

**Returns**:

  Tuple of (AppsApi, ServicesApi, InstancesApi, CatalogInstancesApi) instances
  

**Raises**:

- `ValueError` - If API token is not provided

<a id="koyeb/sandbox.utils.build_env_vars"></a>

#### build\_env\_vars

```python
def build_env_vars(env: Optional[Dict[str, str]]) -> List[DeploymentEnv]
```

Build environment variables list from dictionary.

**Arguments**:

- `env` - Dictionary of environment variables
  

**Returns**:

  List of DeploymentEnv objects

<a id="koyeb/sandbox.utils.create_docker_source"></a>

#### create\_docker\_source

```python
def create_docker_source(image: str,
                         command_args: List[str],
                         privileged: Optional[bool] = None) -> DockerSource
```

Create Docker source configuration.

**Arguments**:

- `image` - Docker image name
- `command_args` - Command and arguments to run (optional, empty list means use image default)
- `privileged` - If True, run the container in privileged mode (default: None/False)
  

**Returns**:

  DockerSource object

<a id="koyeb/sandbox.utils.create_koyeb_sandbox_ports"></a>

#### create\_koyeb\_sandbox\_ports

```python
def create_koyeb_sandbox_ports(protocol: str = "http") -> List[DeploymentPort]
```

Create port configuration for koyeb/sandbox image.

Creates two ports:
- Port 3030 exposed on HTTP, mounted on /koyeb-sandbox/
- Port 3031 exposed with the specified protocol, mounted on /

**Arguments**:

- `protocol` - Protocol to use for port 3031 ("http" or "http2"), defaults to "http"
  

**Returns**:

  List of DeploymentPort objects configured for koyeb/sandbox

<a id="koyeb/sandbox.utils.create_koyeb_sandbox_proxy_ports"></a>

#### create\_koyeb\_sandbox\_proxy\_ports

```python
def create_koyeb_sandbox_proxy_ports() -> List[DeploymentProxyPort]
```

Create TCP proxy port configuration for koyeb/sandbox image.

Creates proxy port for direct TCP access:
- Port 3031 exposed via TCP proxy

**Returns**:

  List of DeploymentProxyPort objects configured for TCP proxy access

<a id="koyeb/sandbox.utils.create_koyeb_sandbox_routes"></a>

#### create\_koyeb\_sandbox\_routes

```python
def create_koyeb_sandbox_routes() -> List[DeploymentRoute]
```

Create route configuration for koyeb/sandbox image to make it publicly accessible.

Creates two routes:
- Port 3030 accessible at /koyeb-sandbox/
- Port 3031 accessible at /

**Returns**:

  List of DeploymentRoute objects configured for koyeb/sandbox

<a id="koyeb/sandbox.utils.create_deployment_definition"></a>

#### create\_deployment\_definition

```python
def create_deployment_definition(
        name: str,
        docker_source: DockerSource,
        env_vars: List[DeploymentEnv],
        instance_type: str,
        exposed_port_protocol: Optional[str] = None,
        region: Optional[str] = None,
        routes: Optional[List[DeploymentRoute]] = None,
        idle_timeout: Optional[IdleTimeout] = None,
        light_sleep_enabled: bool = True,
        enable_tcp_proxy: bool = False) -> DeploymentDefinition
```

Create deployment definition for a sandbox service.

**Arguments**:

- `name` - Service name
- `docker_source` - Docker configuration
- `env_vars` - Environment variables
- `instance_type` - Instance type
- `exposed_port_protocol` - Protocol to expose ports with ("http" or "http2").
  If None, defaults to "http".
  If provided, must be one of "http" or "http2".
- `region` - Region to deploy to (defaults to "na")
- `routes` - List of routes for public access
- `idle_timeout` - Idle timeout configuration (see IdleTimeout type)
- `light_sleep_enabled` - Whether light sleep is enabled for the instance type (default: True)
- `enable_tcp_proxy` - If True, enables TCP proxy for direct TCP access to port 3031
  

**Returns**:

  DeploymentDefinition object

<a id="koyeb/sandbox.utils.get_sandbox_status"></a>

#### get\_sandbox\_status

```python
def get_sandbox_status(instance_id: str,
                       api_token: Optional[str] = None) -> InstanceStatus
```

Get the current status of a sandbox instance.

<a id="koyeb/sandbox.utils.is_sandbox_healthy"></a>

#### is\_sandbox\_healthy

```python
def is_sandbox_healthy(instance_id: str,
                       sandbox_url: str,
                       sandbox_secret: str,
                       api_token: Optional[str] = None) -> bool
```

Check if sandbox is healthy and ready for operations.

This function requires both sandbox_url and sandbox_secret to properly check:
1. The Koyeb instance status (via API) - using instance_id and api_token
2. The sandbox executor health endpoint (via SandboxClient) - using sandbox_url and sandbox_secret

**Arguments**:

- `instance_id` - The Koyeb instance ID
- `api_token` - Koyeb API token
- `sandbox_url` - URL of the sandbox executor API (required)
- `sandbox_secret` - Secret for sandbox executor authentication (required)
  

**Returns**:

- `bool` - True if sandbox is healthy, False otherwise
  

**Raises**:

- `ValueError` - If sandbox_url or sandbox_secret are not provided

<a id="koyeb/sandbox.utils.escape_shell_arg"></a>

#### escape\_shell\_arg

```python
def escape_shell_arg(arg: str) -> str
```

Escape a shell argument for safe use in shell commands.

**Arguments**:

- `arg` - The argument to escape
  

**Returns**:

  Properly escaped shell argument

<a id="koyeb/sandbox.utils.validate_port"></a>

#### validate\_port

```python
def validate_port(port: int) -> None
```

Validate that a port number is in the valid range.

**Arguments**:

- `port` - Port number to validate
  

**Raises**:

- `ValueError` - If port is not in valid range [1, 65535]

<a id="koyeb/sandbox.utils.check_error_message"></a>

#### check\_error\_message

```python
def check_error_message(error_msg: str, error_type: str) -> bool
```

Check if an error message matches a specific error type.
Uses case-insensitive matching against known error patterns.

**Arguments**:

- `error_msg` - The error message to check
- `error_type` - The type of error to check for (key in ERROR_MESSAGES)
  

**Returns**:

  True if error message matches the error type

<a id="koyeb/sandbox.utils.run_sync_in_executor"></a>

#### run\_sync\_in\_executor

```python
async def run_sync_in_executor(method: Callable[..., Any], *args: Any,
                               **kwargs: Any) -> Any
```

Run a synchronous method in an async executor.

Helper function to wrap synchronous methods for async execution.
Used by AsyncSandbox and AsyncSandboxFilesystem to wrap sync parent methods.

**Arguments**:

- `method` - The synchronous method to run
- `*args` - Positional arguments for the method
- `**kwargs` - Keyword arguments for the method
  

**Returns**:

  Result of the synchronous method call

<a id="koyeb/sandbox.utils.async_wrapper"></a>

#### async\_wrapper

```python
def async_wrapper(method_name: str)
```

Decorator to automatically create async wrapper for sync methods.

This decorator creates an async method that wraps a sync method from the parent class.
The sync method is called via super() and executed in an executor.

**Arguments**:

- `method_name` - Name of the sync method to wrap (from parent class)
  
  Usage:
  @async_wrapper("delete")
  async def delete(self) -> None:
  """Delete the sandbox instance asynchronously."""
  pass  # Implementation is handled by decorator

<a id="koyeb/sandbox.utils.create_sandbox_client"></a>

#### create\_sandbox\_client

```python
def create_sandbox_client(sandbox_url: Optional[str],
                          sandbox_secret: Optional[str],
                          existing_client: Optional[Any] = None) -> Any
```

Create or return existing SandboxClient instance with validation.

Helper function to create SandboxClient instances with consistent validation.
Used by Sandbox, SandboxExecutor, and SandboxFilesystem to avoid duplication.

**Arguments**:

- `sandbox_url` - The sandbox URL (from _get_sandbox_url() or sandbox._get_sandbox_url())
- `sandbox_secret` - The sandbox secret
- `existing_client` - Existing client instance to return if not None
  

**Returns**:

- `SandboxClient` - Configured client instance
  

**Raises**:

- `SandboxError` - If sandbox URL or secret is not available

<a id="koyeb/sandbox.utils.SandboxError"></a>

## SandboxError Objects

```python
class SandboxError(Exception)
```

Base exception for sandbox operations

<a id="koyeb/sandbox.utils.SandboxTimeoutError"></a>

## SandboxTimeoutError Objects

```python
class SandboxTimeoutError(SandboxError)
```

Raised when a sandbox operation times out

<a id="koyeb/sandbox.executor_client"></a>

# koyeb/sandbox.executor\_client

Sandbox Executor API Client

A simple Python client for interacting with the Sandbox Executor API.

<a id="koyeb/sandbox.executor_client.SandboxClient"></a>

## SandboxClient Objects

```python
class SandboxClient()
```

Client for the Sandbox Executor API.

<a id="koyeb/sandbox.executor_client.SandboxClient.__init__"></a>

#### \_\_init\_\_

```python
def __init__(base_url: str,
             secret: str,
             timeout: float = DEFAULT_HTTP_TIMEOUT)
```

Initialize the Sandbox Client.

**Arguments**:

- `base_url` - The base URL of the sandbox server (e.g., 'http://localhost:8080')
- `secret` - The authentication secret/token
- `timeout` - Request timeout in seconds (default: 30)

<a id="koyeb/sandbox.executor_client.SandboxClient.close"></a>

#### close

```python
def close() -> None
```

Close the HTTP session and release resources.

<a id="koyeb/sandbox.executor_client.SandboxClient.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__()
```

Context manager entry - returns self.

<a id="koyeb/sandbox.executor_client.SandboxClient.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(exc_type, exc_val, exc_tb) -> None
```

Context manager exit - automatically closes the session.

<a id="koyeb/sandbox.executor_client.SandboxClient.__del__"></a>

#### \_\_del\_\_

```python
def __del__()
```

Clean up session on deletion (fallback, not guaranteed to run).

<a id="koyeb/sandbox.executor_client.SandboxClient.health"></a>

#### health

```python
def health() -> Dict[str, str]
```

Check the health status of the server.

**Returns**:

  Dict with status information
  

**Raises**:

- `requests.HTTPError` - If the health check fails

<a id="koyeb/sandbox.executor_client.SandboxClient.run"></a>

#### run

```python
def run(cmd: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None) -> Dict[str, Any]
```

Execute a shell command in the sandbox.

**Arguments**:

- `cmd` - The shell command to execute
- `cwd` - Optional working directory for command execution
- `env` - Optional environment variables to set/override
- `timeout` - Optional timeout in seconds for the request
  

**Returns**:

  Dict containing stdout, stderr, error (if any), and exit code

<a id="koyeb/sandbox.executor_client.SandboxClient.run_streaming"></a>

#### run\_streaming

```python
def run_streaming(cmd: str,
                  cwd: Optional[str] = None,
                  env: Optional[Dict[str, str]] = None,
                  timeout: Optional[float] = None) -> Iterator[Dict[str, Any]]
```

Execute a shell command in the sandbox and stream the output in real-time.

This method uses Server-Sent Events (SSE) to stream command output line-by-line
as it's produced. Use this for long-running commands where you want real-time
output. For simple commands where buffered output is acceptable, use run() instead.

**Arguments**:

- `cmd` - The shell command to execute
- `cwd` - Optional working directory for command execution
- `env` - Optional environment variables to set/override
- `timeout` - Optional timeout in seconds for the streaming request
  

**Yields**:

  Dict events with the following types:
  
  - output events (as command produces output):
- `{"stream"` - "stdout"|"stderr", "data": "line of output"}
  
  - complete event (when command finishes):
- `{"code"` - <exit_code>, "error": false}
  
  - error event (if command fails to start):
- `{"error"` - "error message"}
  

**Example**:

  >>> client = SandboxClient("http://localhost:8080", "secret")
  >>> for event in client.run_streaming("echo 'Hello'; sleep 1; echo 'World'"):
  ...     if "stream" in event:
  ...         print(f"{event['stream']}: {event['data']}")
  ...     elif "code" in event:
  ...         print(f"Exit code: {event['code']}")

<a id="koyeb/sandbox.executor_client.SandboxClient.write_file"></a>

#### write\_file

```python
def write_file(path: str, content: str) -> Dict[str, Any]
```

Write content to a file.

**Arguments**:

- `path` - The file path to write to
- `content` - The content to write
  

**Returns**:

  Dict with success status and error if any

<a id="koyeb/sandbox.executor_client.SandboxClient.read_file"></a>

#### read\_file

```python
def read_file(path: str) -> Dict[str, Any]
```

Read content from a file.

**Arguments**:

- `path` - The file path to read from
  

**Returns**:

  Dict with file content and error if any

<a id="koyeb/sandbox.executor_client.SandboxClient.delete_file"></a>

#### delete\_file

```python
def delete_file(path: str) -> Dict[str, Any]
```

Delete a file.

**Arguments**:

- `path` - The file path to delete
  

**Returns**:

  Dict with success status and error if any

<a id="koyeb/sandbox.executor_client.SandboxClient.make_dir"></a>

#### make\_dir

```python
def make_dir(path: str) -> Dict[str, Any]
```

Create a directory (including parent directories).

**Arguments**:

- `path` - The directory path to create
  

**Returns**:

  Dict with success status and error if any

<a id="koyeb/sandbox.executor_client.SandboxClient.delete_dir"></a>

#### delete\_dir

```python
def delete_dir(path: str) -> Dict[str, Any]
```

Recursively delete a directory and all its contents.

**Arguments**:

- `path` - The directory path to delete
  

**Returns**:

  Dict with success status and error if any

<a id="koyeb/sandbox.executor_client.SandboxClient.list_dir"></a>

#### list\_dir

```python
def list_dir(path: str) -> Dict[str, Any]
```

List the contents of a directory.

**Arguments**:

- `path` - The directory path to list
  

**Returns**:

  Dict with entries list and error if any

<a id="koyeb/sandbox.executor_client.SandboxClient.bind_port"></a>

#### bind\_port

```python
def bind_port(port: int) -> Dict[str, Any]
```

Bind a port to the TCP proxy for external access.

Configures the TCP proxy to forward traffic to the specified port inside the sandbox.
This allows you to expose services running inside the sandbox to external connections.

**Arguments**:

- `port` - The port number to bind to (must be a valid port number)
  

**Returns**:

  Dict with success status, message, and port information
  

**Notes**:

  - Only one port can be bound at a time
  - Binding a new port will override the previous binding
  - The port must be available and accessible within the sandbox environment

<a id="koyeb/sandbox.executor_client.SandboxClient.unbind_port"></a>

#### unbind\_port

```python
def unbind_port(port: Optional[int] = None) -> Dict[str, Any]
```

Unbind a port from the TCP proxy.

Removes the TCP proxy port binding, stopping traffic forwarding to the previously bound port.

**Arguments**:

- `port` - Optional port number to unbind. If provided, it must match the currently bound port.
  If not provided, any existing binding will be removed.
  

**Returns**:

  Dict with success status and message
  

**Notes**:

  - If a port is specified and doesn't match the currently bound port, the request will fail
  - After unbinding, the TCP proxy will no longer forward traffic

<a id="koyeb/sandbox.executor_client.SandboxClient.start_process"></a>

#### start\_process

```python
def start_process(cmd: str,
                  cwd: Optional[str] = None,
                  env: Optional[Dict[str, str]] = None) -> Dict[str, Any]
```

Start a background process in the sandbox.

Starts a long-running background process that continues executing even after
the API call completes. Use this for servers, workers, or other long-running tasks.

**Arguments**:

- `cmd` - The shell command to execute as a background process
- `cwd` - Optional working directory for the process
- `env` - Optional environment variables to set/override for the process
  

**Returns**:

  Dict with process id and success status:
  - id: The unique process ID (UUID string)
  - success: True if the process was started successfully
  

**Example**:

  >>> client = SandboxClient("http://localhost:8080", "secret")
  >>> result = client.start_process("python -u server.py")
  >>> process_id = result["id"]
  >>> print(f"Started process: {process_id}")

<a id="koyeb/sandbox.executor_client.SandboxClient.kill_process"></a>

#### kill\_process

```python
def kill_process(process_id: str) -> Dict[str, Any]
```

Kill a background process by its ID.

Terminates a running background process. This sends a SIGTERM signal to the process,
allowing it to clean up gracefully. If the process doesn't terminate within a timeout,
it will be forcefully killed with SIGKILL.

**Arguments**:

- `process_id` - The unique process ID (UUID string) to kill
  

**Returns**:

  Dict with success status and error message if any
  

**Example**:

  >>> client = SandboxClient("http://localhost:8080", "secret")
  >>> result = client.kill_process("550e8400-e29b-41d4-a716-446655440000")
  >>> if result.get("success"):
  ...     print("Process killed successfully")

<a id="koyeb/sandbox.executor_client.SandboxClient.list_processes"></a>

#### list\_processes

```python
def list_processes() -> Dict[str, Any]
```

List all background processes.

Returns information about all currently running and recently completed background
processes. This includes both active processes and processes that have completed
(which remain in memory until server restart).

**Returns**:

  Dict with a list of processes:
  - processes: List of process objects, each containing:
  - id: Process ID (UUID string)
  - command: The command that was executed
  - status: Process status (e.g., "running", "completed")
  - pid: OS process ID (if running)
  - exit_code: Exit code (if completed)
  - started_at: ISO 8601 timestamp when process started
  - completed_at: ISO 8601 timestamp when process completed (if applicable)
  

**Example**:

  >>> client = SandboxClient("http://localhost:8080", "secret")
  >>> result = client.list_processes()
  >>> for process in result.get("processes", []):
  ...     print(f"{process['id']}: {process['command']} - {process['status']}")

