<a id="koyeb/sandbox"></a>

# koyeb/sandbox

Koyeb Sandbox - Interactive execution environment for running arbitrary code on Koyeb

<a id="koyeb/sandbox.exec"></a>

# koyeb/sandbox.exec

Command execution utilities for Koyeb Sandbox instances
Using WebSocket connection to Koyeb API

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
- `timeout` - Command timeout in seconds
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
- `timeout` - Command timeout in seconds
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
Using only the primitives available in the Koyeb API

<a id="koyeb/sandbox.filesystem.SandboxFilesystemError"></a>

## SandboxFilesystemError Objects

```python
class SandboxFilesystemError(SandboxError)
```

Base exception for filesystem operations

<a id="koyeb/sandbox.filesystem.FileNotFoundError"></a>

## FileNotFoundError Objects

```python
class FileNotFoundError(SandboxFilesystemError)
```

Raised when file or directory not found

<a id="koyeb/sandbox.filesystem.FileExistsError"></a>

## FileExistsError Objects

```python
class FileExistsError(SandboxFilesystemError)
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
Using only the primitives available in the Koyeb API.

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
- `recursive` - Create parent directories if needed (default: False)

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
def upload_file(local_path: str, remote_path: str) -> None
```

Upload a local file to the sandbox synchronously.

**Arguments**:

- `local_path` - Path to the local file
- `remote_path` - Destination path in the sandbox

<a id="koyeb/sandbox.filesystem.SandboxFilesystem.download_file"></a>

#### download\_file

```python
def download_file(remote_path: str, local_path: str) -> None
```

Download a file from the sandbox to a local path synchronously.

**Arguments**:

- `remote_path` - Path to the file in the sandbox
- `local_path` - Destination path on the local filesystem

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
def open(path: str, mode: str = "r") -> "SandboxFileIO"
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
async def mkdir(path: str, recursive: bool = False) -> None
```

Create a directory asynchronously.

**Arguments**:

- `path` - Absolute path to the directory
- `recursive` - Create parent directories if needed (default: False)

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.list_dir"></a>

#### list\_dir

```python
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
async def delete_file(path: str) -> None
```

Delete a file asynchronously.

**Arguments**:

- `path` - Absolute path to the file

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.delete_dir"></a>

#### delete\_dir

```python
async def delete_dir(path: str) -> None
```

Delete a directory asynchronously.

**Arguments**:

- `path` - Absolute path to the directory

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.rename_file"></a>

#### rename\_file

```python
async def rename_file(old_path: str, new_path: str) -> None
```

Rename a file asynchronously.

**Arguments**:

- `old_path` - Current file path
- `new_path` - New file path

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.move_file"></a>

#### move\_file

```python
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
async def exists(path: str) -> bool
```

Check if file/directory exists asynchronously

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.is_file"></a>

#### is\_file

```python
async def is_file(path: str) -> bool
```

Check if path is a file asynchronously

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.is_dir"></a>

#### is\_dir

```python
async def is_dir(path: str) -> bool
```

Check if path is a directory asynchronously

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.upload_file"></a>

#### upload\_file

```python
async def upload_file(local_path: str, remote_path: str) -> None
```

Upload a local file to the sandbox asynchronously.

**Arguments**:

- `local_path` - Path to the local file
- `remote_path` - Destination path in the sandbox

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.download_file"></a>

#### download\_file

```python
async def download_file(remote_path: str, local_path: str) -> None
```

Download a file from the sandbox to a local path asynchronously.

**Arguments**:

- `remote_path` - Path to the file in the sandbox
- `local_path` - Destination path on the local filesystem

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
async def rm(path: str, recursive: bool = False) -> None
```

Remove file or directory asynchronously.

**Arguments**:

- `path` - Path to remove
- `recursive` - Remove recursively

<a id="koyeb/sandbox.filesystem.AsyncSandboxFilesystem.open"></a>

#### open

```python
def open(path: str, mode: str = "r") -> "AsyncSandboxFileIO"
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

<a id="koyeb/sandbox.sandbox.Sandbox"></a>

## Sandbox Objects

```python
class Sandbox()
```

Synchronous sandbox for running code on Koyeb infrastructure.
Provides creation and deletion functionality with proper health polling.

<a id="koyeb/sandbox.sandbox.Sandbox.create"></a>

#### create

```python
@classmethod
def create(cls,
           image: str = "docker.io/library/ubuntu:latest",
           name: str = "quick-sandbox",
           wait_ready: bool = True,
           instance_type: str = "nano",
           ports: Optional[List[DeploymentPort]] = None,
           env: Optional[Dict[str, str]] = None,
           regions: Optional[List[str]] = None,
           api_token: Optional[str] = None,
           timeout: int = 300) -> "Sandbox"
```

Create a new sandbox instance.

**Arguments**:

- `image` - Docker image to use (default: ubuntu:latest)
- `name` - Name of the sandbox
- `wait_ready` - Wait for sandbox to be ready (default: True)
- `instance_type` - Instance type (default: nano)
- `ports` - List of ports to expose
- `env` - Environment variables
- `regions` - List of regions to deploy to (default: ["na"])
- `api_token` - Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
- `timeout` - Timeout for sandbox creation in seconds
  

**Returns**:

- `Sandbox` - A new Sandbox instance

<a id="koyeb/sandbox.sandbox.Sandbox.wait_ready"></a>

#### wait\_ready

```python
def wait_ready(timeout: int = 60, poll_interval: float = 2.0) -> bool
```

Wait for sandbox to become ready with proper polling.

**Arguments**:

- `timeout` - Maximum time to wait in seconds
- `poll_interval` - Time between health checks in seconds
  

**Returns**:

- `bool` - True if sandbox became ready, False if timeout

<a id="koyeb/sandbox.sandbox.Sandbox.delete"></a>

#### delete

```python
def delete() -> None
```

Delete the sandbox instance.

<a id="koyeb/sandbox.sandbox.Sandbox.status"></a>

#### status

```python
def status() -> str
```

Get current sandbox status

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
def filesystem()
```

Get filesystem operations interface

<a id="koyeb/sandbox.sandbox.Sandbox.exec"></a>

#### exec

```python
@property
def exec()
```

Get command execution interface

<a id="koyeb/sandbox.sandbox.AsyncSandbox"></a>

## AsyncSandbox Objects

```python
class AsyncSandbox(Sandbox)
```

Async sandbox for running code on Koyeb infrastructure.
Inherits from Sandbox and provides async wrappers for all operations.

<a id="koyeb/sandbox.sandbox.AsyncSandbox.create"></a>

#### create

```python
@classmethod
async def create(cls,
                 image: str = "docker.io/library/ubuntu:latest",
                 name: str = "quick-sandbox",
                 wait_ready: bool = True,
                 instance_type: str = "nano",
                 ports: Optional[List[DeploymentPort]] = None,
                 env: Optional[Dict[str, str]] = None,
                 regions: Optional[List[str]] = None,
                 api_token: Optional[str] = None,
                 timeout: int = 300) -> "AsyncSandbox"
```

Create a new sandbox instance with async support.

**Arguments**:

- `image` - Docker image to use (default: ubuntu:latest)
- `name` - Name of the sandbox
- `wait_ready` - Wait for sandbox to be ready (default: True)
- `instance_type` - Instance type (default: nano)
- `ports` - List of ports to expose
- `env` - Environment variables
- `regions` - List of regions to deploy to (default: ["na"])
- `api_token` - Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
- `timeout` - Timeout for sandbox creation in seconds
  

**Returns**:

- `AsyncSandbox` - A new AsyncSandbox instance

<a id="koyeb/sandbox.sandbox.AsyncSandbox.wait_ready"></a>

#### wait\_ready

```python
async def wait_ready(timeout: int = 60, poll_interval: float = 2.0) -> bool
```

Wait for sandbox to become ready with proper async polling.

**Arguments**:

- `timeout` - Maximum time to wait in seconds
- `poll_interval` - Time between health checks in seconds
  

**Returns**:

- `bool` - True if sandbox became ready, False if timeout

<a id="koyeb/sandbox.sandbox.AsyncSandbox.delete"></a>

#### delete

```python
async def delete() -> None
```

Delete the sandbox instance asynchronously.

<a id="koyeb/sandbox.sandbox.AsyncSandbox.status"></a>

#### status

```python
async def status() -> str
```

Get current sandbox status asynchronously

<a id="koyeb/sandbox.sandbox.AsyncSandbox.is_healthy"></a>

#### is\_healthy

```python
async def is_healthy() -> bool
```

Check if sandbox is healthy and ready for operations asynchronously

<a id="koyeb/sandbox.sandbox.AsyncSandbox.exec"></a>

#### exec

```python
@property
def exec()
```

Get async command execution interface

<a id="koyeb/sandbox.sandbox.AsyncSandbox.filesystem"></a>

#### filesystem

```python
@property
def filesystem()
```

Get filesystem operations interface

<a id="koyeb/sandbox.utils"></a>

# koyeb/sandbox.utils

Utility functions for Koyeb Sandbox

<a id="koyeb/sandbox.utils.get_api_client"></a>

#### get\_api\_client

```python
def get_api_client(
        api_token: Optional[str] = None,
        host: Optional[str] = None
) -> tuple[AppsApi, ServicesApi, InstancesApi]
```

Get configured API clients for Koyeb operations.

**Arguments**:

- `api_token` - Koyeb API token. If not provided, will try to get from KOYEB_API_TOKEN env var
- `host` - Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)
  

**Returns**:

  Tuple of (AppsApi, ServicesApi, InstancesApi) instances
  

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
def create_docker_source(image: str, command_args: List[str]) -> DockerSource
```

Create Docker source configuration.

**Arguments**:

- `image` - Docker image name
- `command_args` - Command and arguments to run
  

**Returns**:

  DockerSource object

<a id="koyeb/sandbox.utils.create_deployment_definition"></a>

#### create\_deployment\_definition

```python
def create_deployment_definition(
        name: str,
        docker_source: DockerSource,
        env_vars: List[DeploymentEnv],
        instance_type: str,
        ports: Optional[List[DeploymentPort]] = None,
        regions: List[str] = None) -> DeploymentDefinition
```

Create deployment definition for a sandbox service.

**Arguments**:

- `name` - Service name
- `docker_source` - Docker configuration
- `env_vars` - Environment variables
- `instance_type` - Instance type
- `ports` - List of ports (if provided, type becomes WEB, otherwise WORKER)
- `regions` - List of regions (defaults to North America)
  

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
                       api_token: Optional[str] = None) -> bool
```

Check if sandbox is healthy and ready for operations.

<a id="koyeb/sandbox.utils.ensure_sandbox_healthy"></a>

#### ensure\_sandbox\_healthy

```python
def ensure_sandbox_healthy(instance_id: str,
                           api_token: Optional[str] = None) -> None
```

Ensure a sandbox instance is healthy, raising an exception if not.

<a id="koyeb/sandbox.utils.SandboxError"></a>

## SandboxError Objects

```python
class SandboxError(Exception)
```

Base exception for sandbox operations

