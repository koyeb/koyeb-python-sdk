<a id="koyeb.sandbox"></a>

# koyeb.sandbox

Koyeb Sandbox - Interactive execution environment for running arbitrary code on Koyeb

<a id="koyeb.sandbox.sandbox"></a>

# koyeb.sandbox.sandbox

Koyeb Sandbox - Python SDK for creating and managing Koyeb sandboxes

<a id="koyeb.sandbox.sandbox.DEFAULT_INSTANCE_WAIT_TIMEOUT"></a>

#### DEFAULT\_INSTANCE\_WAIT\_TIMEOUT

seconds

<a id="koyeb.sandbox.sandbox.DEFAULT_POLL_INTERVAL"></a>

#### DEFAULT\_POLL\_INTERVAL

seconds

<a id="koyeb.sandbox.sandbox.ProcessInfo"></a>

## ProcessInfo Objects

```python
@dataclass
class ProcessInfo()
```

Type definition for process information returned by list_processes.

<a id="koyeb.sandbox.sandbox.ProcessInfo.id"></a>

#### id

Process ID (UUID string)

<a id="koyeb.sandbox.sandbox.ProcessInfo.command"></a>

#### command

The command that was executed

<a id="koyeb.sandbox.sandbox.ProcessInfo.status"></a>

#### status

Process status (e.g., "running", "completed")

<a id="koyeb.sandbox.sandbox.ProcessInfo.pid"></a>

#### pid

OS process ID (if running)

<a id="koyeb.sandbox.sandbox.ProcessInfo.exit_code"></a>

#### exit\_code

Exit code (if completed)

<a id="koyeb.sandbox.sandbox.ProcessInfo.started_at"></a>

#### started\_at

ISO 8601 timestamp when process started

<a id="koyeb.sandbox.sandbox.ProcessInfo.completed_at"></a>

#### completed\_at

ISO 8601 timestamp when process completed (if applicable)

<a id="koyeb.sandbox.sandbox.ExposedPort"></a>

## ExposedPort Objects

```python
@dataclass
class ExposedPort()
```

Result of exposing a port via TCP proxy.

<a id="koyeb.sandbox.sandbox.validate_port"></a>

#### validate\_port

```python
def validate_port(port: int) -> None
```

Validate that a port number is in the valid range.

**Arguments**:

- `port` - Port number to validate
  

**Raises**:

- `ValueError` - If port is not in valid range [1, 65535]

<a id="koyeb.sandbox.sandbox.Sandbox"></a>

## Sandbox Objects

```python
class Sandbox()
```

Synchronous sandbox for running code on Koyeb infrastructure.
Provides creation and deletion functionality with proper health polling.

<a id="koyeb.sandbox.sandbox.Sandbox.id"></a>

#### id

```python
@property
def id() -> str
```

Get the service ID of the sandbox.

<a id="koyeb.sandbox.sandbox.Sandbox.create"></a>

#### create

```python
@classmethod
def create(cls,
           image: str = "koyeb/sandbox",
           name: str = "quick-sandbox",
           wait_ready: bool = True,
           instance_type: str = "micro",
           exposed_port_protocol: Optional[str] = None,
           env: Optional[Dict[str, Any]] = None,
           config_files: Optional[Dict[str, Any]] = None,
           region: Optional[str] = None,
           api_token: Optional[str] = None,
           timeout: int = 300,
           idle_timeout: int = 300,
           enable_tcp_proxy: bool = False,
           privileged: bool = False,
           registry_secret: Optional[str] = None,
           _experimental_enable_light_sleep: bool = False,
           _experimental_deep_sleep_value: int = 3900,
           delete_after_delay: int = 0,
           delete_after_inactivity_delay: int = 0,
           app_id: Optional[str] = None,
           enable_mesh: Optional[bool] = None,
           poll_interval: float = DEFAULT_POLL_INTERVAL,
           entrypoint: Optional[List[str]] = None,
           command: Optional[str] = None,
           args: Optional[List[str]] = None,
           host: Optional[str] = None,
           block_network: bool = False,
           outbound_allowlist: Optional[List[str]] = None,
           snapshot: Optional[Union[str, "Snapshot"]] = None,
           sandbox_secret: Optional[str] = None,
           cleanup_on_failure: bool = True) -> Sandbox
```

Create a new sandbox instance.

**Arguments**:

- `image` - Docker image to use (default: koyeb/sandbox)
- `name` - Name of the sandbox
- `wait_ready` - Wait for sandbox to be ready (default: True)
- `instance_type` - Instance type (default: micro)
- `exposed_port_protocol` - Protocol to expose ports with ("http" or "http2").
  If None, defaults to "http".
  If provided, must be one of "http" or "http2".
- `env` - Environment variables
- `config_files` - Config files to create in the sandbox, as a dictionary mapping
  file paths to file contents. Values can be plain strings (default permissions 0644)
  or ``ConfigFile`` instances for custom permissions
  (e.g., {"/etc/myapp/config.yaml": "key: value", "/etc/myapp/cert.pem": ConfigFile(content="...", permissions="0600")})
- `region` - Region to deploy to. Defaults to KOYEB_REGION env var, or "na" if not set.
- `api_token` - Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
- `timeout` - Timeout for sandbox creation in seconds
- `idle_timeout` - Sleep timeout in seconds. Behavior depends on _experimental_enable_light_sleep:
  - If _experimental_enable_light_sleep is True: sets light_sleep value (deep_sleep=3900)
  - If _experimental_enable_light_sleep is False: sets deep_sleep value
  - If 0: disables scale-to-zero (keep always-on)
- `enable_tcp_proxy` - If True, enables TCP proxy for direct TCP access to port 3031
- `privileged` - If True, run the container in privileged mode (default: False)
- `registry_secret` - Name of a Koyeb secret containing registry credentials for
  pulling private images. Create the secret via Koyeb dashboard or CLI first.
- `_experimental_enable_light_sleep` - If True, uses idle_timeout for light_sleep and sets
  deep_sleep=3900. If False, uses idle_timeout for deep_sleep (default: False)
- `delete_after_delay` - If >0, automatically delete the sandbox if there was no activity
  after this many seconds since creation.
- `delete_after_inactivity_delay` - If >0, automatically delete the sandbox if service sleeps due to inactivity
  after this many seconds.
- `app_id` - If provided, create the sandbox service in an existing app instead of creating a new one.
- `enable_mesh` - Mesh tri-state: None (default) = auto, True = enabled, False = disabled
- `poll_interval` - Time between health checks in seconds when wait_ready is True (default: 0.5)
- `entrypoint` - Override the default entrypoint of the Docker image (e.g., ["/bin/sh", "-c"])
- `command` - Override the default command of the Docker image (e.g., "python app.py")
- `host` - Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)
- `block_network` - If True, block all outbound network access from the sandbox
- `outbound_allowlist` - List of IPs/CIDRs allowed as outbound destinations;
  all other outbound traffic is blocked. Bare IPs are normalized to
  /32 (IPv4) or /128 (IPv6). Mutually exclusive with block_network.
- `snapshot` - Optional. A Snapshot object or snapshot name/ID string to create the sandbox from.
  If provided, the sandbox will be initialized from this snapshot.
  Can be either a Snapshot object (e.g., snapshot=my_snapshot) or a snapshot name/ID string (e.g., snapshot="my snapshot").
- `sandbox_secret` - Optional sandbox secret to use for executor authentication. If not provided, a new one will be generated.
  

**Returns**:

- `Sandbox` - A new Sandbox instance
  

**Raises**:

- `ValueError` - If API token is not provided
- `SandboxTimeoutError` - If wait_ready is True and sandbox does not become ready within timeout
- `EgressPolicyError` - If both block_network and outbound_allowlist are passed,
  or an allowlist entry is not a valid IP address or CIDR
  

**Example**:

  >>> # Public image (default)
  >>> sandbox = Sandbox.create()
  
  >>> # Private image with registry secret
  >>> sandbox = Sandbox.create(
  ...     image="ghcr.io/myorg/myimage:latest",
  ...     registry_secret="my-ghcr-secret"
  ... )
  
  >>> # Create from a Snapshot object
  >>> from koyeb.sandbox import Snapshot
  >>> snapshot = Snapshot.get("my-snapshot-id")
  >>> sandbox = Sandbox.create(snapshot=snapshot)
  
  >>> # Create from a snapshot ID string
  >>> sandbox = Sandbox.create(snapshot="my-snapshot-id")
  
  >>> # Create from a snapshot with custom parameters
  >>> sandbox = Sandbox.create(
  ...     snapshot="my-snapshot-id",
  ...     image="python:3.12",
  ...     instance_type="nano",
  ...     env={"MY_VAR": "value"}
  ... )

<a id="koyeb.sandbox.sandbox.Sandbox.get_from_id"></a>

#### get\_from\_id

```python
@classmethod
def get_from_id(cls,
                id: str,
                api_token: Optional[str] = None,
                host: Optional[str] = None) -> "Sandbox"
```

Get a sandbox by service ID.

**Arguments**:

- `id` - Service ID of the sandbox
- `api_token` - Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
- `host` - Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)
  

**Returns**:

- `Sandbox` - The Sandbox instance
  

**Raises**:

- `ValueError` - If API token is not provided or id is invalid
- `SandboxError` - If sandbox is not found or retrieval fails

<a id="koyeb.sandbox.sandbox.Sandbox.list"></a>

#### list

```python
@classmethod
def list(cls,
         app_id: Optional[str] = None,
         name: Optional[str] = None,
         api_token: Optional[str] = None,
         host: Optional[str] = None) -> List["Sandbox"]
```

List sandbox services.

Paginates services of type SANDBOX (100 per page, mirroring the CLI).
Returns lazily-connected handles: they carry no executor secret, so
connected operations raise NoSandboxSecretError — use
``Sandbox.get_from_id(handle.id)`` for a connected handle.

**Arguments**:

- `app_id` - Optional app filter
- `name` - Optional name filter
- `api_token` - Koyeb API token (defaults to KOYEB_API_TOKEN env var)
- `host` - Koyeb API host (defaults to KOYEB_API_HOST env var)
  

**Returns**:

- `List[Sandbox]` - Lazy handles for every sandbox service

<a id="koyeb.sandbox.sandbox.Sandbox.snapshot"></a>

#### snapshot

```python
def snapshot(name: str,
             snapshot_type: Optional["SnapshotType"] = None,
             wait_available: bool = True,
             timeout: int = 600) -> "Snapshot"
```

Create a snapshot of this sandbox.

Captures the current state of the sandbox's filesystem (and optionally
running processes for FULL type) so it can be restored later.

**Arguments**:

- `name` - Name for the snapshot
- `snapshot_type` - Type of snapshot to create (FILESYSTEM or FULL).
  Defaults to FILESYSTEM.
- `wait_available` - Whether to wait for snapshot to become available
- `timeout` - Timeout in seconds for waiting
  

**Returns**:

- `Snapshot` - The created snapshot object
  

**Raises**:

- `SandboxError` - If snapshot creation fails

<a id="koyeb.sandbox.sandbox.Sandbox.create_from_snapshot"></a>

#### create\_from\_snapshot

```python
@classmethod
def create_from_snapshot(cls,
                         snapshot: Union["Snapshot", str],
                         name: Optional[str] = None,
                         wait_ready: bool = True,
                         timeout: int = 300,
                         **create_kwargs) -> "Sandbox"
```

Create a new sandbox from a snapshot.

**Arguments**:

- `snapshot` - Snapshot object or snapshot ID string
- `name` - Name for the new sandbox
- `wait_ready` - Whether to wait for sandbox to be ready
- `timeout` - Timeout in seconds
- `**create_kwargs` - Additional arguments to pass to create()
  

**Returns**:

- `Sandbox` - A new sandbox instance

<a id="koyeb.sandbox.sandbox.Sandbox.template"></a>

#### template

```python
@classmethod
def template(cls,
             name: str,
             image: str,
             workdir: Optional[str] = None,
             api_token: Optional[str] = None,
             host: Optional[str] = None,
             delete_builder: bool = True) -> "DeclarativeSnapshot"
```

Create a declarative snapshot builder.

Use this to build a reusable snapshot by declaratively defining
the sandbox environment (files, packages, etc.) and then building
a snapshot that can be used to spawn pre-configured sandboxes.

**Arguments**:

- `name` - Name for the template
- `image` - Docker image to use
- `workdir` - Working directory in the sandbox
- `api_token` - Koyeb API token
- `host` - Koyeb API host
- `delete_builder` - Whether to delete the builder sandbox after creating the snapshot (default: True)
  

**Returns**:

- `DeclarativeSnapshot` - Fluent builder for creating snapshots
  

**Example**:

  snapshot = (
  Sandbox.template("python-ci", image="python:3.12", workdir="/workspace")
  .file("requirements.txt", "pytest\nrequests")
  .run("pip install -r requirements.txt")
  .build(snapshot_name="python-ci-env")
  )
  
  sbx = snapshot.spawn(name="test-runner")

<a id="koyeb.sandbox.sandbox.Sandbox.wait_ready"></a>

#### wait\_ready

```python
def wait_ready(timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
               poll_interval: Optional[float] = None) -> bool
```

Wait for sandbox to become ready with exponential backoff polling.

First waits for the deployment status to become HEALTHY, then polls the
sandbox health endpoint to confirm the executor is responsive.

Starts polling at 0.1s intervals, doubling each time up to poll_interval.

**Arguments**:

- `timeout` - Maximum time to wait in seconds
- `poll_interval` - Maximum time between health checks in seconds (defaults to instance poll_interval)
  

**Returns**:

- `bool` - True if sandbox became ready, False if timeout

<a id="koyeb.sandbox.sandbox.Sandbox.wait_tcp_proxy_ready"></a>

#### wait\_tcp\_proxy\_ready

```python
def wait_tcp_proxy_ready(timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
                         poll_interval: Optional[float] = None) -> bool
```

Wait for TCP proxy to become ready and available.

Polls the deployment metadata with exponential backoff until the TCP proxy
information is available. Starts at 0.1s intervals, doubling up to poll_interval.

**Arguments**:

- `timeout` - Maximum time to wait in seconds
- `poll_interval` - Maximum time between checks in seconds (defaults to instance poll_interval)
  

**Returns**:

- `bool` - True if TCP proxy became ready, False if timeout

<a id="koyeb.sandbox.sandbox.Sandbox.delete"></a>

#### delete

```python
def delete() -> None
```

Delete the sandbox instance.

Deletes the whole app for SDK-created sandboxes; only the service
when the sandbox lives in a caller-provided app.

<a id="koyeb.sandbox.sandbox.Sandbox.get_domain"></a>

#### get\_domain

```python
def get_domain() -> Optional[str]
```

Get the public domain of the sandbox.

Returns the domain (e.g., "app-name-org.koyeb.app/r/routing_key/" or
"app-name-org.koyeb.app") without protocol. To get the full URL with protocol,
use sandbox._get_url()

**Returns**:

- `Optional[str]` - The domain or None if unavailable

<a id="koyeb.sandbox.sandbox.Sandbox.get_tcp_proxy_info"></a>

#### get\_tcp\_proxy\_info

```python
def get_tcp_proxy_info() -> Optional[tuple[str, int]]
```

Get the TCP proxy host and port for the sandbox.

Returns the TCP proxy host and port as a tuple (host, port) for direct TCP access to port 3031.
This is only available if enable_tcp_proxy=True was set when creating the sandbox.

**Returns**:

  Optional[tuple[str, int]]: A tuple of (host, port) or None if unavailable

<a id="koyeb.sandbox.sandbox.Sandbox.is_healthy"></a>

#### is\_healthy

```python
def is_healthy() -> bool
```

Check if sandbox is healthy and ready for operations.

Raises SandboxDeploymentError when the deployment reached a terminal
state (e.g. STOPPED) — classification fails closed.

<a id="koyeb.sandbox.sandbox.Sandbox.filesystem"></a>

#### filesystem

```python
@property
def filesystem() -> "SandboxFilesystem"
```

Get filesystem operations interface

<a id="koyeb.sandbox.sandbox.Sandbox.exec"></a>

#### exec

```python
@property
def exec() -> "SandboxExecutor"
```

Get command execution interface

<a id="koyeb.sandbox.sandbox.Sandbox.expose_port"></a>

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

<a id="koyeb.sandbox.sandbox.Sandbox.unexpose_port"></a>

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

<a id="koyeb.sandbox.sandbox.Sandbox.launch_process"></a>

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

<a id="koyeb.sandbox.sandbox.Sandbox.kill_process"></a>

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

<a id="koyeb.sandbox.sandbox.Sandbox.list_processes"></a>

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

<a id="koyeb.sandbox.sandbox.Sandbox.kill_all_processes"></a>

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

<a id="koyeb.sandbox.sandbox.Sandbox.update_lifecycle"></a>

#### update\_lifecycle

```python
def update_lifecycle(delete_after_delay: Optional[int] = None,
                     delete_after_inactivity: Optional[int] = None) -> None
```

Update the sandbox's life cycle settings.

**Arguments**:

- `delete_after_delay` - If >0, automatically delete the sandbox if there was no activity
  after this many seconds since creation.
- `delete_after_inactivity` - If >0, automatically delete the sandbox if service sleeps due to inactivity
  after this many seconds.
  

**Raises**:

- `SandboxError` - If updating life cycle fails
  

**Example**:

  >>> sandbox.update_life_cycle(delete_after_delay=600, delete_after_inactivity=300)

<a id="koyeb.sandbox.sandbox.Sandbox.update_network_policy"></a>

#### update\_network\_policy

```python
def update_network_policy(
        block_network: bool = False,
        outbound_allowlist: Optional[List[str]] = None) -> None
```

Update the sandbox's network policy.

Warning: applying a new network policy triggers a redeployment of the
sandbox service. The sandbox is restarted and any in-memory or
non-persisted state is lost. This method does not wait for the
redeployment to finish; it repoints the sandbox at the new deployment
and clears cached connection state, so call wait_ready() afterwards to
block until the replacement deployment is healthy before issuing further
operations.

**Arguments**:

- `block_network` - If True, block all outbound network access from the sandbox
- `outbound_allowlist` - List of IPs/CIDRs allowed as outbound destinations;
  all other outbound traffic is blocked. Bare IPs are normalized to
  /32 (IPv4) or /128 (IPv6). Mutually exclusive with block_network.
  
  With both arguments unset, the network policy is reset to the
  platform default (unrestricted outbound access).
  

**Raises**:

- `EgressPolicyError` - If both block_network and outbound_allowlist are
  passed, or an allowlist entry is not a valid IP address or CIDR
- `SandboxError` - If updating the network policy fails
  

**Example**:

  >>> sandbox.update_network_policy(block_network=True)
  >>> sandbox.update_network_policy(outbound_allowlist=["10.0.0.0/8", "1.2.3.4"])
  >>> sandbox.update_network_policy()  # reset to unrestricted

<a id="koyeb.sandbox.sandbox.Sandbox.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__() -> "Sandbox"
```

Context manager entry - returns self.

<a id="koyeb.sandbox.sandbox.Sandbox.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(exc_type, exc_val, exc_tb) -> None
```

Context manager exit - automatically deletes the sandbox.

<a id="koyeb.sandbox.sandbox.AsyncSandbox"></a>

## AsyncSandbox Objects

```python
class AsyncSandbox(Sandbox)
```

Async sandbox for running code on Koyeb infrastructure.
Inherits from Sandbox and provides native async implementations.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.get_from_id"></a>

#### get\_from\_id

```python
@classmethod
async def get_from_id(cls,
                      id: str,
                      api_token: Optional[str] = None,
                      host: Optional[str] = None) -> "AsyncSandbox"
```

Get a sandbox by service ID asynchronously.

**Arguments**:

- `id` - Service ID of the sandbox
- `api_token` - Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
- `host` - Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)
  

**Returns**:

- `AsyncSandbox` - The AsyncSandbox instance
  

**Raises**:

- `ValueError` - If API token is not provided or id is invalid
- `SandboxError` - If sandbox is not found or retrieval fails

<a id="koyeb.sandbox.sandbox.AsyncSandbox.create"></a>

#### create

```python
@classmethod
async def create(cls,
                 image: str = "koyeb/sandbox",
                 name: str = "quick-sandbox",
                 wait_ready: bool = True,
                 instance_type: str = "micro",
                 exposed_port_protocol: Optional[str] = None,
                 env: Optional[Dict[str, Any]] = None,
                 config_files: Optional[Dict[str, Any]] = None,
                 region: Optional[str] = None,
                 api_token: Optional[str] = None,
                 timeout: int = 300,
                 idle_timeout: int = 300,
                 enable_tcp_proxy: bool = False,
                 privileged: bool = False,
                 registry_secret: Optional[str] = None,
                 _experimental_enable_light_sleep: bool = False,
                 _experimental_deep_sleep_value: int = 3900,
                 delete_after_delay: int = 0,
                 delete_after_inactivity_delay: int = 0,
                 app_id: Optional[str] = None,
                 enable_mesh: Optional[bool] = None,
                 poll_interval: float = DEFAULT_POLL_INTERVAL,
                 entrypoint: Optional[List[str]] = None,
                 command: Optional[str] = None,
                 args: Optional[List[str]] = None,
                 host: Optional[str] = None,
                 block_network: bool = False,
                 outbound_allowlist: Optional[List[str]] = None,
                 snapshot: Optional[Union[str, "Snapshot"]] = None,
                 sandbox_secret: Optional[str] = None,
                 cleanup_on_failure: bool = True) -> AsyncSandbox
```

Create a new sandbox instance with async support.

**Arguments**:

- `image` - Docker image to use (default: koyeb/sandbox)
- `name` - Name of the sandbox
- `wait_ready` - Wait for sandbox to be ready (default: True)
- `instance_type` - Instance type (default: micro)
- `exposed_port_protocol` - Protocol to expose ports with ("http" or "http2").
  If None, defaults to "http".
  If provided, must be one of "http" or "http2".
- `env` - Environment variables
- `config_files` - Config files to create in the sandbox, as a dictionary mapping
  file paths to file contents. Values can be plain strings (default permissions 0644)
  or ``ConfigFile`` instances for custom permissions
  (e.g., {"/etc/myapp/config.yaml": "key: value", "/etc/myapp/cert.pem": ConfigFile(content="...", permissions="0600")})
- `region` - Region to deploy to. Defaults to KOYEB_REGION env var, or "na" if not set.
- `api_token` - Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
- `timeout` - Timeout for sandbox creation in seconds
- `idle_timeout` - Sleep timeout in seconds. Behavior depends on _experimental_enable_light_sleep:
  - If _experimental_enable_light_sleep is True: sets light_sleep value (deep_sleep uses _experimental_deep_sleep_value)
  - If _experimental_enable_light_sleep is False: sets deep_sleep value
  - If 0: disables scale-to-zero (keep always-on)
- `enable_tcp_proxy` - If True, enables TCP proxy for direct TCP access to port 3031
- `privileged` - If True, run the container in privileged mode (default: False)
- `registry_secret` - Name of a Koyeb secret containing registry credentials for
  pulling private images. Create the secret via Koyeb dashboard or CLI first.
- `_experimental_enable_light_sleep` - If True, uses idle_timeout for light_sleep and configurable
  deep_sleep (default: False)
- `_experimental_deep_sleep_value` - Number of seconds for deep sleep when light sleep is enabled (default: 3900).
  Only used if _experimental_enable_light_sleep is True
- `delete_after_delay` - If >0, automatically delete the sandbox if there was no activity
  after this many seconds since creation.
- `delete_after_inactivity_delay` - If >0, automatically delete the sandbox if service sleeps due to inactivity
  after this many seconds.
- `app_id` - If provided, create the sandbox service in an existing app instead of creating a new one.
- `enable_mesh` - Mesh tri-state: None (default) = auto, True = enabled, False = disabled
- `poll_interval` - Time between health checks in seconds when wait_ready is True (default: 0.5)
- `entrypoint` - Override the default entrypoint of the Docker image (e.g., ["/bin/sh", "-c"])
- `command` - Override the default command of the Docker image (e.g., "python app.py")
- `host` - Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)
- `block_network` - If True, block all outbound network access from the sandbox
- `outbound_allowlist` - List of IPs/CIDRs allowed as outbound destinations;
  all other outbound traffic is blocked. Bare IPs are normalized to
  /32 (IPv4) or /128 (IPv6). Mutually exclusive with block_network.
- `snapshot` - Optional. A Snapshot object or snapshot name/ID string to create the sandbox from.
  If provided, the sandbox will be initialized from this snapshot.
  Can be either a Snapshot object (e.g., snapshot=my_snapshot) or a snapshot name/ID string (e.g., snapshot="my snapshot").
- `sandbox_secret` - Optional sandbox secret to use for executor authentication. If not provided, a new one will be generated.
  

**Returns**:

- `AsyncSandbox` - A new AsyncSandbox instance
  

**Raises**:

- `ValueError` - If API token is not provided
- `SandboxTimeoutError` - If wait_ready is True and sandbox does not become ready within timeout
- `EgressPolicyError` - If both block_network and outbound_allowlist are passed,
  or an allowlist entry is not a valid IP address or CIDR

<a id="koyeb.sandbox.sandbox.AsyncSandbox.list"></a>

#### list

```python
@classmethod
async def list(cls,
               app_id: Optional[str] = None,
               name: Optional[str] = None,
               api_token: Optional[str] = None,
               host: Optional[str] = None) -> List["AsyncSandbox"]
```

List sandbox services (async twin of :meth:`Sandbox.list`).

Returns lazily-connected handles without executor secrets; use
``AsyncSandbox.get_from_id(handle.id)`` for a connected handle.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.wait_ready"></a>

#### wait\_ready

```python
async def wait_ready(timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
                     poll_interval: Optional[float] = None) -> bool
```

Wait for sandbox to become ready with exponential backoff async polling.

First waits for the deployment status to become HEALTHY, then polls the
sandbox health endpoint to confirm the executor is responsive.

Starts polling at 0.1s intervals, doubling each time up to poll_interval.

**Arguments**:

- `timeout` - Maximum time to wait in seconds
- `poll_interval` - Maximum time between health checks in seconds (defaults to instance poll_interval)
  

**Returns**:

- `bool` - True if sandbox became ready, False if timeout

<a id="koyeb.sandbox.sandbox.AsyncSandbox.wait_tcp_proxy_ready"></a>

#### wait\_tcp\_proxy\_ready

```python
async def wait_tcp_proxy_ready(timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
                               poll_interval: Optional[float] = None) -> bool
```

Wait for TCP proxy to become ready and available asynchronously.

Polls the deployment metadata with exponential backoff until the TCP proxy
information is available. Starts at 0.1s intervals, doubling up to poll_interval.

**Arguments**:

- `timeout` - Maximum time to wait in seconds
- `poll_interval` - Maximum time between checks in seconds (defaults to instance poll_interval)
  

**Returns**:

- `bool` - True if TCP proxy became ready, False if timeout

<a id="koyeb.sandbox.sandbox.AsyncSandbox.delete"></a>

#### delete

```python
async def delete() -> None
```

Delete the sandbox instance asynchronously.

Deletes the whole app for SDK-created sandboxes; only the service
when the sandbox lives in a caller-provided app.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.snapshot"></a>

#### snapshot

```python
async def snapshot(name: str,
                   snapshot_type: Optional["SnapshotType"] = None,
                   wait_available: bool = True,
                   timeout: int = 600) -> "Snapshot"
```

Create a snapshot of this sandbox asynchronously.

Captures the current state of the sandbox's filesystem (and optionally
running processes for FULL type) so it can be restored later.

**Arguments**:

- `name` - Name for the snapshot
- `snapshot_type` - Type of snapshot to create (FILESYSTEM or FULL).
  Defaults to FILESYSTEM.
- `wait_available` - Whether to wait for snapshot to become available
- `timeout` - Timeout in seconds for waiting
  

**Returns**:

- `Snapshot` - The created snapshot object
  

**Raises**:

- `SandboxError` - If snapshot creation fails

<a id="koyeb.sandbox.sandbox.AsyncSandbox.create_from_snapshot"></a>

#### create\_from\_snapshot

```python
@classmethod
async def create_from_snapshot(cls,
                               snapshot: Union["Snapshot", str],
                               name: Optional[str] = None,
                               wait_ready: bool = True,
                               timeout: int = 300,
                               **create_kwargs) -> "AsyncSandbox"
```

Create a new async sandbox from a snapshot.

**Arguments**:

- `snapshot` - Snapshot object or snapshot ID string
- `name` - Name for the new sandbox
- `wait_ready` - Whether to wait for sandbox to be ready
- `timeout` - Timeout in seconds
- `**create_kwargs` - Additional arguments to pass to create()
  

**Returns**:

- `AsyncSandbox` - A new async sandbox instance

<a id="koyeb.sandbox.sandbox.AsyncSandbox.is_healthy"></a>

#### is\_healthy

```python
async def is_healthy() -> bool
```

Check if sandbox is healthy and ready for operations asynchronously.

Raises SandboxDeploymentError when the deployment reached a terminal
state (e.g. STOPPED) — classification fails closed.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.exec"></a>

#### exec

```python
@property
def exec() -> "AsyncSandboxExecutor"
```

Get async command execution interface

<a id="koyeb.sandbox.sandbox.AsyncSandbox.filesystem"></a>

#### filesystem

```python
@property
def filesystem() -> "AsyncSandboxFilesystem"
```

Get filesystem operations interface

<a id="koyeb.sandbox.sandbox.AsyncSandbox.expose_port"></a>

#### expose\_port

```python
async def expose_port(port: int) -> ExposedPort
```

Expose a port to external connections via TCP proxy asynchronously.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.unexpose_port"></a>

#### unexpose\_port

```python
async def unexpose_port() -> None
```

Unexpose a port from external connections asynchronously.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.launch_process"></a>

#### launch\_process

```python
async def launch_process(cmd: str,
                         cwd: Optional[str] = None,
                         env: Optional[Dict[str, str]] = None) -> str
```

Launch a background process in the sandbox asynchronously.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.kill_process"></a>

#### kill\_process

```python
async def kill_process(process_id: str) -> None
```

Kill a background process by its ID asynchronously.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.list_processes"></a>

#### list\_processes

```python
async def list_processes() -> List[ProcessInfo]
```

List all background processes asynchronously.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.kill_all_processes"></a>

#### kill\_all\_processes

```python
async def kill_all_processes() -> int
```

Kill all running background processes asynchronously.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.update_lifecycle"></a>

#### update\_lifecycle

```python
async def update_lifecycle(
        delete_after_delay: Optional[int] = None,
        delete_after_inactivity: Optional[int] = None) -> None
```

Update the sandbox's life cycle settings asynchronously.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.update_network_policy"></a>

#### update\_network\_policy

```python
async def update_network_policy(
        block_network: bool = False,
        outbound_allowlist: Optional[List[str]] = None) -> None
```

Update the sandbox's network policy asynchronously.

Warning: applying a new network policy triggers a redeployment of the
sandbox service. The sandbox is restarted and any in-memory or
non-persisted state is lost. This method does not wait for the
redeployment to finish; it repoints the sandbox at the new deployment
and clears cached connection state, so call wait_ready() afterwards to
block until the replacement deployment is healthy before issuing further
operations.

See Sandbox.update_network_policy for full documentation.

**Raises**:

- `EgressPolicyError` - If both block_network and outbound_allowlist are
  passed, or an allowlist entry is not a valid IP address or CIDR
- `SandboxError` - If updating the network policy fails

<a id="koyeb.sandbox.sandbox.AsyncSandbox.__aenter__"></a>

#### \_\_aenter\_\_

```python
async def __aenter__() -> "AsyncSandbox"
```

Async context manager entry - returns self.

<a id="koyeb.sandbox.sandbox.AsyncSandbox.__aexit__"></a>

#### \_\_aexit\_\_

```python
async def __aexit__(exc_type, exc_val, exc_tb) -> None
```

Async context manager exit - automatically deletes the sandbox.

<a id="koyeb.sandbox.spec"></a>

# koyeb.sandbox.spec

SandboxSpec: the create vocabulary for Koyeb sandboxes.

One definition of a sandbox deployment — env/secret injection, mesh
tri-state, scale-to-zero sleep, ports/routes, snapshot branches. Every
create flow (sync and async, Sandbox and ServicePool) builds one spec and
consumes its payloads, so the decision logic lives here exactly once.

<a id="koyeb.sandbox.spec.build_env_vars"></a>

#### build\_env\_vars

```python
def build_env_vars(env: Optional[Dict[str, Any]]) -> List[DeploymentEnv]
```

Build environment variables list from dictionary.

**Arguments**:

- `env` - Dictionary of environment variables. Values can be plain strings
  or ``Secret`` instances. A ``Secret`` value is rendered as
  ``"{{ secret.<name> }}"`` so the Koyeb API substitutes the secret
  value at deploy time.
  

**Returns**:

  List of DeploymentEnv objects

<a id="koyeb.sandbox.spec.build_config_files"></a>

#### build\_config\_files

```python
def build_config_files(
        config_files: Optional[Dict[str, Any]]) -> List[ConfigFile]
```

Build config files list from dictionary.

**Arguments**:

- `config_files` - Dictionary mapping file paths to file contents.
  Values can be plain strings (default permissions 0644) or
  ``ConfigFile`` instances (custom permissions). The dict key is
  always used as the file path.
  

**Returns**:

  List of ConfigFile objects

<a id="koyeb.sandbox.spec.create_docker_source"></a>

#### create\_docker\_source

```python
def create_docker_source(image: str,
                         privileged: Optional[bool] = None,
                         image_registry_secret: Optional[str] = None,
                         entrypoint: Optional[List[str]] = None,
                         command: Optional[str] = None,
                         args: Optional[List[str]] = None) -> DockerSource
```

Create Docker source configuration.

**Arguments**:

- `image` - Docker image name
- `privileged` - If True, run the container in privileged mode (default: None/False)
- `image_registry_secret` - Name of the secret containing registry credentials
  for pulling private images
- `entrypoint` - Override the default entrypoint of the Docker image
- `command` - Override the default command of the Docker image
- `args` - Arguments to pass to the command
  

**Returns**:

  DockerSource object

<a id="koyeb.sandbox.spec.create_koyeb_sandbox_ports"></a>

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

<a id="koyeb.sandbox.spec.create_koyeb_sandbox_proxy_ports"></a>

#### create\_koyeb\_sandbox\_proxy\_ports

```python
def create_koyeb_sandbox_proxy_ports() -> List[DeploymentProxyPort]
```

Create TCP proxy port configuration for koyeb/sandbox image.

Creates proxy port for direct TCP access:
- Port 3031 exposed via TCP proxy

**Returns**:

  List of DeploymentProxyPort objects configured for TCP proxy access

<a id="koyeb.sandbox.spec.create_koyeb_sandbox_routes"></a>

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

<a id="koyeb.sandbox.spec.create_deployment_definition"></a>

#### create\_deployment\_definition

```python
def create_deployment_definition(
        name: str,
        docker_source: DockerSource,
        env_vars: List[DeploymentEnv],
        instance_type: str,
        definition_type: DeploymentDefinitionType = DeploymentDefinitionType.
    SANDBOX,
        ports: Optional[List[DeploymentPort]] = None,
        exposed_port_protocol: Optional[str] = None,
        region: Optional[str] = None,
        routes: Optional[List[DeploymentRoute]] = None,
        idle_timeout: int = 300,
        enable_tcp_proxy: bool = False,
        _experimental_enable_light_sleep: bool = False,
        _experimental_deep_sleep_value: int = 3900,
        enable_mesh: Optional[bool] = None,
        config_files: Optional[List[ConfigFile]] = None,
        network_policy: Optional[NetworkPolicy] = None
) -> DeploymentDefinition
```

Create deployment definition for a sandbox service.

**Arguments**:

- `name` - Service name
- `docker_source` - Docker configuration
- `env_vars` - Environment variables
- `instance_type` - Instance type
- `definition_type` - Deployment definition type. SANDBOX (the default) keeps
  the sandbox auto-wiring (ports 3030/3031 and the sandbox routes);
  every other type carries only caller-supplied ports/routes.
- `ports` - Caller-supplied ports (non-SANDBOX definitions); SANDBOX always
  wires its own 3030/3031 pair.
- `exposed_port_protocol` - Protocol to expose ports with ("http" or "http2").
  If None, defaults to "http".
  If provided, must be one of "http" or "http2".
- `region` - Region to deploy to. Defaults to KOYEB_REGION env var, or "na" if not set.
- `routes` - List of routes for public access
- `idle_timeout` - Number of seconds to wait before sleeping the instance if it receives no traffic
- `enable_tcp_proxy` - If True, enables TCP proxy for direct TCP access to port 3031
- `_experimental_enable_light_sleep` - If True, uses light sleep when reaching idle_timeout.
  Light Sleep reduces cold starts to ~200ms. After scaling to zero, the service stays in Light Sleep for idle_timeout seconds before going into Deep Sleep.
- `_experimental_deep_sleep_value` - Number of seconds for deep sleep when light sleep is enabled (default: 3900).
  Only used if _experimental_enable_light_sleep is True. Ignored otherwise.
- `enable_mesh` - Mesh tri-state: None (default) = auto, True = enabled, False = disabled
- `network_policy` - Optional network policy restricting egress traffic
  

**Returns**:

  DeploymentDefinition object

<a id="koyeb.sandbox.spec.SandboxSpec"></a>

## SandboxSpec Objects

```python
@dataclass
class SandboxSpec()
```

The single definition of a sandbox deployment.

``definition_type`` defaults to SANDBOX, which keeps the sandbox
auto-wiring; pool flows set WEB/WORKER and carry their own ports and
routes. Invalid egress or port protocol fails at construction, before
any API call. Sandbox flows call apply_sandbox_secret() before
deployment_definition(): the secret rides the env. Pool flows never
inject one — the platform mints the executor secret.

<a id="koyeb.sandbox.spec.SandboxSpec.apply_sandbox_secret"></a>

#### apply\_sandbox\_secret

```python
def apply_sandbox_secret(sandbox_secret: Optional[str] = None) -> str
```

Generate when missing, inject into env, return the secret.

<a id="koyeb.sandbox.spec.SandboxSpec.app_payload"></a>

#### app\_payload

```python
def app_payload() -> Dict[str, Any]
```

CreateApp payload for the app a create call owns.

<a id="koyeb.sandbox.spec.SandboxSpec.deployment_definition"></a>

#### deployment\_definition

```python
def deployment_definition() -> DeploymentDefinition
```

The deployment definition; the sync model is the wire truth.

<a id="koyeb.sandbox.spec.SandboxSpec.deployment_definition_dict"></a>

#### deployment\_definition\_dict

```python
def deployment_definition_dict() -> Dict[str, Any]
```

Wire-format definition; both model flavors coerce this dict.

<a id="koyeb.sandbox.spec.SandboxSpec.service_life_cycle"></a>

#### service\_life\_cycle

```python
def service_life_cycle() -> Dict[str, Any]
```

ServiceLifeCycle payload.

<a id="koyeb.sandbox.spec.SandboxSpec.create_service_payload"></a>

#### create\_service\_payload

```python
def create_service_payload(app_id: str) -> Dict[str, Any]
```

CreateService payload. FULL snapshots omit the definition (the
API infers it); every other shape pins one.

<a id="koyeb.sandbox.control_plane"></a>

# koyeb.sandbox.control\_plane

The control-plane seam: the narrow interface between the sandbox layer
and the Koyeb API.

Two adapters share the orchestration above them — the generated
koyeb.api (sync) and koyeb.api_async (async) clients — so the sandbox
twins never touch model flavors again: neutral info types come out,
payload dicts go in. Errors map to SandboxError exactly where the
orchestration contract demands it (service lookup); raw ApiException
propagates where callers clean up (create/delete/update).

<a id="koyeb.sandbox.control_plane.AppInfo"></a>

## AppInfo Objects

```python
@dataclass(frozen=True)
class AppInfo()
```

Neutral app summary.

<a id="koyeb.sandbox.control_plane.ServiceInfo"></a>

## ServiceInfo Objects

```python
@dataclass(frozen=True)
class ServiceInfo()
```

Neutral service summary.

<a id="koyeb.sandbox.control_plane.DeploymentInfo"></a>

## DeploymentInfo Objects

```python
@dataclass(frozen=True)
class DeploymentInfo()
```

Neutral deployment summary.

status stays raw (enum or string) for classify_deployment_status;
env is flattened for SANDBOX_SECRET extraction. The definition dict
is its own seam op (deployment_definition) so wait-polling paths
never pay for serialization.

<a id="koyeb.sandbox.control_plane.SyncControlPlane"></a>

## SyncControlPlane Objects

```python
class SyncControlPlane()
```

Control-plane adapter over the generated koyeb.api clients.

<a id="koyeb.sandbox.control_plane.AsyncControlPlane"></a>

## AsyncControlPlane Objects

```python
class AsyncControlPlane()
```

Control-plane adapter over the generated koyeb.api_async clients.

<a id="koyeb.sandbox.exec"></a>

# koyeb.sandbox.exec

Command execution utilities for Koyeb Sandbox instances
Using SandboxClient HTTP API

<a id="koyeb.sandbox.exec.CommandStatus"></a>

## CommandStatus Objects

```python
class CommandStatus(str, Enum)
```

Command execution status

<a id="koyeb.sandbox.exec.CommandResult"></a>

## CommandResult Objects

```python
@dataclass
class CommandResult()
```

Result of a command execution using Koyeb API models

<a id="koyeb.sandbox.exec.CommandResult.success"></a>

#### success

```python
@property
def success() -> bool
```

Check if command executed successfully

<a id="koyeb.sandbox.exec.CommandResult.output"></a>

#### output

```python
@property
def output() -> str
```

Get combined stdout and stderr output

<a id="koyeb.sandbox.exec.SandboxCommandError"></a>

## SandboxCommandError Objects

```python
class SandboxCommandError(SandboxError)
```

Raised when a sandbox command fails (opt-in via raise_on_error).

<a id="koyeb.sandbox.exec._EventFold"></a>

## \_EventFold Objects

```python
class _EventFold()
```

Folds executor stream events into a CommandResult.

The sync and async exec twins differ only in how events are pulled;
this class owns what every event means.

<a id="koyeb.sandbox.exec._EventFold.feed"></a>

#### feed

```python
def feed(event: Dict[str, Any]) -> Optional[CommandResult]
```

Consume one event; returns a result only for a failed start.

<a id="koyeb.sandbox.exec.SandboxExecutor"></a>

## SandboxExecutor Objects

```python
class SandboxExecutor()
```

Synchronous command execution interface for Koyeb Sandbox instances.
Bound to a specific sandbox instance.

For async usage, use AsyncSandboxExecutor instead.

<a id="koyeb.sandbox.exec.SandboxExecutor.__call__"></a>

#### \_\_call\_\_

```python
def __call__(command: str,
             cwd: Optional[str] = None,
             env: Optional[Dict[str, str]] = None,
             timeout: int = 30,
             on_stdout: Optional[Callable[[str], None]] = None,
             on_stderr: Optional[Callable[[str], None]] = None,
             stream: bool = True,
             raise_on_error: bool = False) -> CommandResult
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

<a id="koyeb.sandbox.exec.AsyncSandboxExecutor"></a>

## AsyncSandboxExecutor Objects

```python
class AsyncSandboxExecutor(SandboxExecutor)
```

Async command execution interface for Koyeb Sandbox instances.
Bound to a specific sandbox instance.

Inherits from SandboxExecutor and provides async command execution
using native async I/O via AsyncSandboxClient.

<a id="koyeb.sandbox.exec.AsyncSandboxExecutor.__call__"></a>

#### \_\_call\_\_

```python
async def __call__(command: str,
                   cwd: Optional[str] = None,
                   env: Optional[Dict[str, str]] = None,
                   timeout: int = 30,
                   on_stdout: Optional[Callable[[str], None]] = None,
                   on_stderr: Optional[Callable[[str], None]] = None,
                   stream: bool = True,
                   raise_on_error: bool = False) -> CommandResult
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

<a id="koyeb.sandbox.executor_client"></a>

# koyeb.sandbox.executor\_client

Sandbox Executor API Client

Sync and async Python clients for interacting with the Sandbox Executor API.

<a id="koyeb.sandbox.executor_client.DEFAULT_HTTP_TIMEOUT"></a>

#### DEFAULT\_HTTP\_TIMEOUT

seconds for HTTP requests

<a id="koyeb.sandbox.executor_client.ConnectionInfo"></a>

## ConnectionInfo Objects

```python
@dataclass
class ConnectionInfo()
```

Information needed to connect to a sandbox

<a id="koyeb.sandbox.executor_client.SandboxClient"></a>

## SandboxClient Objects

```python
class SandboxClient()
```

Client for the Sandbox Executor API.

<a id="koyeb.sandbox.executor_client.SandboxClient.__init__"></a>

#### \_\_init\_\_

```python
def __init__(conn_info: ConnectionInfo, timeout: float = DEFAULT_HTTP_TIMEOUT)
```

Initialize the Sandbox Client.

**Arguments**:

- `conn_info` - The parameters needed to connect to the sandbox
- `timeout` - Request timeout in seconds (default: 30)

<a id="koyeb.sandbox.executor_client.SandboxClient.close"></a>

#### close

```python
def close() -> None
```

Close the HTTP client and release resources.

<a id="koyeb.sandbox.executor_client.SandboxClient.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__()
```

Context manager entry - returns self.

<a id="koyeb.sandbox.executor_client.SandboxClient.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(exc_type, exc_val, exc_tb) -> None
```

Context manager exit - automatically closes the client.

<a id="koyeb.sandbox.executor_client.SandboxClient.__del__"></a>

#### \_\_del\_\_

```python
def __del__()
```

Clean up client on deletion (fallback, not guaranteed to run).

<a id="koyeb.sandbox.executor_client.SandboxClient.health"></a>

#### health

```python
def health() -> Dict[str, str]
```

Check the health status of the server.

Uses a short timeout and no retries since callers (wait_ready)
already handle polling with backoff.

**Returns**:

  Dict with status information
  

**Raises**:

- `httpx.HTTPStatusError` - If the health check fails
- `httpx.TimeoutException` - If the health check times out

<a id="koyeb.sandbox.executor_client.SandboxClient.run"></a>

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

<a id="koyeb.sandbox.executor_client.SandboxClient.run_streaming"></a>

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

<a id="koyeb.sandbox.executor_client.SandboxClient.write_file"></a>

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

<a id="koyeb.sandbox.executor_client.SandboxClient.read_file"></a>

#### read\_file

```python
def read_file(path: str) -> Dict[str, Any]
```

Read content from a file.

**Arguments**:

- `path` - The file path to read from
  

**Returns**:

  Dict with file content and error if any

<a id="koyeb.sandbox.executor_client.SandboxClient.delete_file"></a>

#### delete\_file

```python
def delete_file(path: str) -> Dict[str, Any]
```

Delete a file.

**Arguments**:

- `path` - The file path to delete
  

**Returns**:

  Dict with success status and error if any

<a id="koyeb.sandbox.executor_client.SandboxClient.make_dir"></a>

#### make\_dir

```python
def make_dir(path: str) -> Dict[str, Any]
```

Create a directory (including parent directories).

**Arguments**:

- `path` - The directory path to create
  

**Returns**:

  Dict with success status and error if any

<a id="koyeb.sandbox.executor_client.SandboxClient.delete_dir"></a>

#### delete\_dir

```python
def delete_dir(path: str) -> Dict[str, Any]
```

Recursively delete a directory and all its contents.

**Arguments**:

- `path` - The directory path to delete
  

**Returns**:

  Dict with success status and error if any

<a id="koyeb.sandbox.executor_client.SandboxClient.list_dir"></a>

#### list\_dir

```python
def list_dir(path: str) -> Dict[str, Any]
```

List the contents of a directory.

**Arguments**:

- `path` - The directory path to list
  

**Returns**:

  Dict with entries list and error if any

<a id="koyeb.sandbox.executor_client.SandboxClient.bind_port"></a>

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

<a id="koyeb.sandbox.executor_client.SandboxClient.unbind_port"></a>

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

<a id="koyeb.sandbox.executor_client.SandboxClient.start_process"></a>

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

<a id="koyeb.sandbox.executor_client.SandboxClient.kill_process"></a>

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

<a id="koyeb.sandbox.executor_client.SandboxClient.list_processes"></a>

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

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient"></a>

## AsyncSandboxClient Objects

```python
class AsyncSandboxClient()
```

Async client for the Sandbox Executor API using httpx.

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.__init__"></a>

#### \_\_init\_\_

```python
def __init__(conn_info: ConnectionInfo, timeout: float = DEFAULT_HTTP_TIMEOUT)
```

Initialize the Async Sandbox Client.

**Arguments**:

- `conn_info` - The parameters needed to connect to the sandbox
- `timeout` - Request timeout in seconds (default: 30)

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.close"></a>

#### close

```python
async def close() -> None
```

Close the HTTP client and release resources.

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.__aenter__"></a>

#### \_\_aenter\_\_

```python
async def __aenter__()
```

Async context manager entry - returns self.

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.__aexit__"></a>

#### \_\_aexit\_\_

```python
async def __aexit__(exc_type, exc_val, exc_tb) -> None
```

Async context manager exit - automatically closes the client.

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.health"></a>

#### health

```python
async def health() -> Dict[str, str]
```

Check the health status of the server.

Uses a short timeout and no retries since callers (wait_ready)
already handle polling with backoff.

**Returns**:

  Dict with status information
  

**Raises**:

- `httpx.HTTPStatusError` - If the health check fails
- `httpx.TimeoutException` - If the health check times out

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.run"></a>

#### run

```python
async def run(cmd: str,
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

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.run_streaming"></a>

#### run\_streaming

```python
async def run_streaming(
        cmd: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None) -> AsyncIterator[Dict[str, Any]]
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

  >>> client = AsyncSandboxClient("http://localhost:8080", "secret")
  >>> async for event in client.run_streaming("echo 'Hello'; sleep 1; echo 'World'"):
  ...     if "stream" in event:
  ...         print(f"{event['stream']}: {event['data']}")
  ...     elif "code" in event:
  ...         print(f"Exit code: {event['code']}")

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.write_file"></a>

#### write\_file

```python
async def write_file(path: str, content: str) -> Dict[str, Any]
```

Write content to a file.

**Arguments**:

- `path` - The file path to write to
- `content` - The content to write
  

**Returns**:

  Dict with success status and error if any

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.read_file"></a>

#### read\_file

```python
async def read_file(path: str) -> Dict[str, Any]
```

Read content from a file.

**Arguments**:

- `path` - The file path to read from
  

**Returns**:

  Dict with file content and error if any

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.delete_file"></a>

#### delete\_file

```python
async def delete_file(path: str) -> Dict[str, Any]
```

Delete a file.

**Arguments**:

- `path` - The file path to delete
  

**Returns**:

  Dict with success status and error if any

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.make_dir"></a>

#### make\_dir

```python
async def make_dir(path: str) -> Dict[str, Any]
```

Create a directory (including parent directories).

**Arguments**:

- `path` - The directory path to create
  

**Returns**:

  Dict with success status and error if any

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.delete_dir"></a>

#### delete\_dir

```python
async def delete_dir(path: str) -> Dict[str, Any]
```

Recursively delete a directory and all its contents.

**Arguments**:

- `path` - The directory path to delete
  

**Returns**:

  Dict with success status and error if any

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.list_dir"></a>

#### list\_dir

```python
async def list_dir(path: str) -> Dict[str, Any]
```

List the contents of a directory.

**Arguments**:

- `path` - The directory path to list
  

**Returns**:

  Dict with entries list and error if any

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.bind_port"></a>

#### bind\_port

```python
async def bind_port(port: int) -> Dict[str, Any]
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

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.unbind_port"></a>

#### unbind\_port

```python
async def unbind_port(port: Optional[int] = None) -> Dict[str, Any]
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

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.start_process"></a>

#### start\_process

```python
async def start_process(
        cmd: str,
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

  >>> client = AsyncSandboxClient("http://localhost:8080", "secret")
  >>> result = await client.start_process("python -u server.py")
  >>> process_id = result["id"]
  >>> print(f"Started process: {process_id}")

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.kill_process"></a>

#### kill\_process

```python
async def kill_process(process_id: str) -> Dict[str, Any]
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

  >>> client = AsyncSandboxClient("http://localhost:8080", "secret")
  >>> result = await client.kill_process("550e8400-e29b-41d4-a716-446655440000")
  >>> if result.get("success"):
  ...     print("Process killed successfully")

<a id="koyeb.sandbox.executor_client.AsyncSandboxClient.list_processes"></a>

#### list\_processes

```python
async def list_processes() -> Dict[str, Any]
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

  >>> client = AsyncSandboxClient("http://localhost:8080", "secret")
  >>> result = await client.list_processes()
  >>> for process in result.get("processes", []):
  ...     print(f"{process['id']}: {process['command']} - {process['status']}")

<a id="koyeb.sandbox.filesystem"></a>

# koyeb.sandbox.filesystem

Filesystem operations for Koyeb Sandbox instances
Using SandboxClient HTTP API

<a id="koyeb.sandbox.filesystem.check_error_message"></a>

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

<a id="koyeb.sandbox.filesystem.escape_shell_arg"></a>

#### escape\_shell\_arg

```python
def escape_shell_arg(arg: str) -> str
```

Escape a shell argument for safe use in shell commands.

**Arguments**:

- `arg` - The argument to escape
  

**Returns**:

  Properly escaped shell argument

<a id="koyeb.sandbox.filesystem.SandboxFilesystemError"></a>

## SandboxFilesystemError Objects

```python
class SandboxFilesystemError(SandboxError)
```

Base exception for filesystem operations

<a id="koyeb.sandbox.filesystem.SandboxFileNotFoundError"></a>

## SandboxFileNotFoundError Objects

```python
class SandboxFileNotFoundError(SandboxFilesystemError)
```

Raised when file or directory not found

<a id="koyeb.sandbox.filesystem.SandboxFileExistsError"></a>

## SandboxFileExistsError Objects

```python
class SandboxFileExistsError(SandboxFilesystemError)
```

Raised when file already exists

<a id="koyeb.sandbox.filesystem.FileInfo"></a>

## FileInfo Objects

```python
@dataclass
class FileInfo()
```

File information

<a id="koyeb.sandbox.filesystem.SandboxFilesystem"></a>

## SandboxFilesystem Objects

```python
class SandboxFilesystem()
```

Synchronous filesystem operations for Koyeb Sandbox instances.
Using SandboxClient HTTP API.

For async usage, use AsyncSandboxFilesystem instead.

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.write_file"></a>

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

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.read_file"></a>

#### read\_file

```python
def read_file(path: str, encoding: str = "utf-8") -> FileInfo
```

Read a file from the sandbox synchronously.

**Arguments**:

- `path` - Absolute path to the file
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary data,
  which will decode the base64 content and return bytes.
  

**Returns**:

- `FileInfo` - Object with content (str or bytes if base64) and encoding

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.mkdir"></a>

#### mkdir

```python
def mkdir(path: str) -> None
```

Create a directory synchronously.

Note: Parent directories are always created automatically by the API.

**Arguments**:

- `path` - Absolute path to the directory

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.list_dir"></a>

#### list\_dir

```python
def list_dir(path: str = ".") -> List[str]
```

List contents of a directory synchronously.

**Arguments**:

- `path` - Path to the directory (default: current directory)
  

**Returns**:

- `List[str]` - Names of files and directories within the specified path.

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.delete_file"></a>

#### delete\_file

```python
def delete_file(path: str) -> None
```

Delete a file synchronously.

**Arguments**:

- `path` - Absolute path to the file

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.delete_dir"></a>

#### delete\_dir

```python
def delete_dir(path: str) -> None
```

Delete a directory synchronously.

**Arguments**:

- `path` - Absolute path to the directory

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.rename_file"></a>

#### rename\_file

```python
def rename_file(old_path: str, new_path: str) -> None
```

Rename a file synchronously.

**Arguments**:

- `old_path` - Current file path
- `new_path` - New file path

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.move_file"></a>

#### move\_file

```python
def move_file(source_path: str, destination_path: str) -> None
```

Move a file to a different directory synchronously.

**Arguments**:

- `source_path` - Current file path
- `destination_path` - Destination path

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.write_files"></a>

#### write\_files

```python
def write_files(files: List[Dict[str, str]]) -> None
```

Write multiple files in a single operation synchronously.

**Arguments**:

- `files` - List of dictionaries, each with 'path', 'content', and optional 'encoding'.

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.exists"></a>

#### exists

```python
def exists(path: str) -> bool
```

Check if file/directory exists synchronously

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.is_file"></a>

#### is\_file

```python
def is_file(path: str) -> bool
```

Check if path is a file synchronously

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.is_dir"></a>

#### is\_dir

```python
def is_dir(path: str) -> bool
```

Check if path is a directory synchronously

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.upload_file"></a>

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

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.download_file"></a>

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

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.ls"></a>

#### ls

```python
def ls(path: str = ".") -> List[str]
```

List directory contents synchronously.

**Arguments**:

- `path` - Path to list
  

**Returns**:

  List of file/directory names

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.rm"></a>

#### rm

```python
def rm(path: str, recursive: bool = False) -> None
```

Remove file or directory synchronously.

**Arguments**:

- `path` - Path to remove
- `recursive` - Remove recursively

<a id="koyeb.sandbox.filesystem.SandboxFilesystem.open"></a>

#### open

```python
def open(path: str, mode: str = "r", encoding: str = "utf-8") -> SandboxFileIO
```

Open a file in the sandbox synchronously.

**Arguments**:

- `path` - Path to the file
- `mode` - Open mode ('r', 'w', 'a', etc.)
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary data.
  

**Returns**:

- `SandboxFileIO` - File handle

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem"></a>

## AsyncSandboxFilesystem Objects

```python
class AsyncSandboxFilesystem(SandboxFilesystem)
```

Async filesystem operations for Koyeb Sandbox instances.
Uses native async I/O via AsyncSandboxClient.

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.write_file"></a>

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

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.read_file"></a>

#### read\_file

```python
async def read_file(path: str, encoding: str = "utf-8") -> FileInfo
```

Read a file from the sandbox asynchronously.

**Arguments**:

- `path` - Absolute path to the file
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary data,
  which will decode the base64 content and return bytes.
  

**Returns**:

- `FileInfo` - Object with content (str or bytes if base64) and encoding

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.mkdir"></a>

#### mkdir

```python
async def mkdir(path: str) -> None
```

Create a directory asynchronously.

Note: Parent directories are always created automatically by the API.

**Arguments**:

- `path` - Absolute path to the directory

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.list_dir"></a>

#### list\_dir

```python
async def list_dir(path: str = ".") -> List[str]
```

List contents of a directory asynchronously.

**Arguments**:

- `path` - Path to the directory (default: current directory)
  

**Returns**:

- `List[str]` - Names of files and directories within the specified path.

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.delete_file"></a>

#### delete\_file

```python
async def delete_file(path: str) -> None
```

Delete a file asynchronously.

**Arguments**:

- `path` - Absolute path to the file

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.delete_dir"></a>

#### delete\_dir

```python
async def delete_dir(path: str) -> None
```

Delete a directory asynchronously.

**Arguments**:

- `path` - Absolute path to the directory

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.rename_file"></a>

#### rename\_file

```python
async def rename_file(old_path: str, new_path: str) -> None
```

Rename a file asynchronously.

**Arguments**:

- `old_path` - Current file path
- `new_path` - New file path

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.move_file"></a>

#### move\_file

```python
async def move_file(source_path: str, destination_path: str) -> None
```

Move a file to a different directory asynchronously.

**Arguments**:

- `source_path` - Current file path
- `destination_path` - Destination path

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.write_files"></a>

#### write\_files

```python
async def write_files(files: List[Dict[str, str]]) -> None
```

Write multiple files in a single operation asynchronously.

**Arguments**:

- `files` - List of dictionaries, each with 'path', 'content', and optional 'encoding'.

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.exists"></a>

#### exists

```python
async def exists(path: str) -> bool
```

Check if file/directory exists asynchronously

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.is_file"></a>

#### is\_file

```python
async def is_file(path: str) -> bool
```

Check if path is a file asynchronously

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.is_dir"></a>

#### is\_dir

```python
async def is_dir(path: str) -> bool
```

Check if path is a directory asynchronously

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.upload_file"></a>

#### upload\_file

```python
async def upload_file(local_path: str,
                      remote_path: str,
                      encoding: str = "utf-8") -> None
```

Upload a local file to the sandbox asynchronously.

**Arguments**:

- `local_path` - Path to the local file
- `remote_path` - Destination path in the sandbox
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary files.
  

**Raises**:

- `SandboxFileNotFoundError` - If local file doesn't exist
- `UnicodeDecodeError` - If file cannot be decoded with specified encoding

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.download_file"></a>

#### download\_file

```python
async def download_file(remote_path: str,
                        local_path: str,
                        encoding: str = "utf-8") -> None
```

Download a file from the sandbox to a local path asynchronously.

**Arguments**:

- `remote_path` - Path to the file in the sandbox
- `local_path` - Destination path on the local filesystem
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary files.
  

**Raises**:

- `SandboxFileNotFoundError` - If remote file doesn't exist

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.ls"></a>

#### ls

```python
async def ls(path: str = ".") -> List[str]
```

List directory contents asynchronously.

**Arguments**:

- `path` - Path to list
  

**Returns**:

  List of file/directory names

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.rm"></a>

#### rm

```python
async def rm(path: str, recursive: bool = False) -> None
```

Remove file or directory asynchronously.

**Arguments**:

- `path` - Path to remove
- `recursive` - Remove recursively

<a id="koyeb.sandbox.filesystem.AsyncSandboxFilesystem.open"></a>

#### open

```python
def open(path: str,
         mode: str = "r",
         encoding: str = "utf-8") -> AsyncSandboxFileIO
```

Open a file in the sandbox asynchronously.

**Arguments**:

- `path` - Path to the file
- `mode` - Open mode ('r', 'w', 'a', etc.)
- `encoding` - File encoding (default: "utf-8"). Use "base64" for binary data.
  

**Returns**:

- `AsyncSandboxFileIO` - Async file handle

<a id="koyeb.sandbox.filesystem.SandboxFileIO"></a>

## SandboxFileIO Objects

```python
class SandboxFileIO()
```

Synchronous file I/O handle for sandbox files

<a id="koyeb.sandbox.filesystem.SandboxFileIO.read"></a>

#### read

```python
def read() -> Union[str, bytes]
```

Read file content synchronously

<a id="koyeb.sandbox.filesystem.SandboxFileIO.write"></a>

#### write

```python
def write(content: Union[str, bytes]) -> None
```

Write content to file synchronously

<a id="koyeb.sandbox.filesystem.SandboxFileIO.close"></a>

#### close

```python
def close() -> None
```

Close the file

<a id="koyeb.sandbox.filesystem.AsyncSandboxFileIO"></a>

## AsyncSandboxFileIO Objects

```python
class AsyncSandboxFileIO()
```

Async file I/O handle for sandbox files

<a id="koyeb.sandbox.filesystem.AsyncSandboxFileIO.read"></a>

#### read

```python
async def read() -> Union[str, bytes]
```

Read file content asynchronously

<a id="koyeb.sandbox.filesystem.AsyncSandboxFileIO.write"></a>

#### write

```python
async def write(content: Union[str, bytes]) -> None
```

Write content to file asynchronously

<a id="koyeb.sandbox.filesystem.AsyncSandboxFileIO.close"></a>

#### close

```python
def close() -> None
```

Close the file

<a id="koyeb.sandbox.pool"></a>

# koyeb.sandbox.pool

Koyeb service pools: pre-warmed sandbox pools and claims.

Mirrors the JS SDK's service-pool.ts / claim.ts: a pool keeps ``size``
pre-warmed services ready; ``claim()`` hands one out idempotently (the
same ``request_id`` returns the same claim), retrying transient failures
(429/5xx) with linear backoff. Sync and async are fully mirrored.

<a id="koyeb.sandbox.pool.DEFAULT_CLAIM_RETRY_DELAY"></a>

#### DEFAULT\_CLAIM\_RETRY\_DELAY

seconds; linear: delay * attempt number

<a id="koyeb.sandbox.pool.ClaimResult"></a>

## ClaimResult Objects

```python
@dataclass
class ClaimResult()
```

A sandbox claimed from a service pool (``service_id`` is always set).

The claimed sandbox is detached from the pool and owned by the caller.

<a id="koyeb.sandbox.pool.claim"></a>

#### claim

```python
def claim(pool_id: str,
          request_id: Optional[str] = None,
          api_token: Optional[str] = None,
          host: Optional[str] = None,
          max_attempts: int = DEFAULT_CLAIM_ATTEMPTS,
          retry_delay: float = DEFAULT_CLAIM_RETRY_DELAY) -> ClaimResult
```

Claim a sandbox from a service pool.

On the warm path (``prewarmed=True``) the claimed sandbox is already
running. On the cold path a sandbox service is created on demand:
``service_id`` is returned immediately and the sandbox becomes usable
once the service is ready — see ``wait_claim_ready``.

The claimed service is detached from the pool and owned by the
caller: delete it like any other sandbox once you are done with it.

Idempotent: the same ``(pool_id, request_id)`` pair always returns the
same claim; ``request_id`` defaults to a generated UUID and is preserved
across the SDK's internal retries.

<a id="koyeb.sandbox.pool.claim_async"></a>

#### claim\_async

```python
async def claim_async(
        pool_id: str,
        request_id: Optional[str] = None,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
        max_attempts: int = DEFAULT_CLAIM_ATTEMPTS,
        retry_delay: float = DEFAULT_CLAIM_RETRY_DELAY) -> ClaimResult
```

Async twin of :func:`claim`.

<a id="koyeb.sandbox.pool.get_claim"></a>

#### get\_claim

```python
def get_claim(claim_id: str,
              api_token: Optional[str] = None,
              host: Optional[str] = None) -> PoolClaim
```

Fetch a claim's state (UNSPECIFIED, PENDING, FULFILLED, FAILED, RELEASED).

<a id="koyeb.sandbox.pool.get_claim_async"></a>

#### get\_claim\_async

```python
async def get_claim_async(claim_id: str,
                          api_token: Optional[str] = None,
                          host: Optional[str] = None) -> Any
```

Async twin of :func:`get_claim`.

<a id="koyeb.sandbox.pool.list_claims"></a>

#### list\_claims

```python
def list_claims(pool_id: str,
                status: Optional[str] = None,
                limit: Optional[int] = None,
                offset: Optional[int] = None,
                api_token: Optional[str] = None,
                host: Optional[str] = None) -> List[PoolClaim]
```

List claims on a service pool, optionally filtered by status.

<a id="koyeb.sandbox.pool.list_claims_async"></a>

#### list\_claims\_async

```python
async def list_claims_async(pool_id: str,
                            status: Optional[str] = None,
                            limit: Optional[int] = None,
                            offset: Optional[int] = None,
                            api_token: Optional[str] = None,
                            host: Optional[str] = None) -> List[Any]
```

Async twin of :func:`list_claims`.

<a id="koyeb.sandbox.pool.wait_claim_ready"></a>

#### wait\_claim\_ready

```python
def wait_claim_ready(claim_or_service_id: Union[ClaimResult, str],
                     timeout: float = DEFAULT_CLAIM_WAIT_TIMEOUT,
                     poll_interval: float = DEFAULT_CLAIM_POLL_INTERVAL,
                     api_token: Optional[str] = None,
                     host: Optional[str] = None) -> bool
```

Poll Get Service until the claimed sandbox is ready.

General service-health polling: returns True on ready, False on
timeout, and raises :class:`ServiceTerminalStateError` on terminal
states. Transient Get Service failures are treated as in-progress and
retried until the timeout (they dominate while a cold claim provisions).

<a id="koyeb.sandbox.pool.wait_claim_ready_async"></a>

#### wait\_claim\_ready\_async

```python
async def wait_claim_ready_async(
        claim_or_service_id: Union[ClaimResult, str],
        timeout: float = DEFAULT_CLAIM_WAIT_TIMEOUT,
        poll_interval: float = DEFAULT_CLAIM_POLL_INTERVAL,
        api_token: Optional[str] = None,
        host: Optional[str] = None) -> bool
```

Async twin of :func:`wait_claim_ready`.

<a id="koyeb.sandbox.pool.ServicePool"></a>

## ServicePool Objects

```python
class ServicePool()
```

A Koyeb service pool keeping pre-warmed sandboxes ready to claim.

<a id="koyeb.sandbox.pool.ServicePool.create"></a>

#### create

```python
@classmethod
def create(cls,
           name: str,
           image: str = "koyeb/sandbox",
           size: int = DEFAULT_POOL_SIZE,
           instance_type: str = "micro",
           region: Optional[str] = None,
           env: Optional[dict] = None,
           config_files: Optional[dict] = None,
           type: str = "SANDBOX",
           entrypoint: Optional[List[str]] = None,
           command: Optional[str] = None,
           args: Optional[List[str]] = None,
           ports: Optional[List[Any]] = None,
           routes: Optional[List[Any]] = None,
           privileged: bool = False,
           registry_secret: Optional[str] = None,
           exposed_port_protocol: Optional[str] = None,
           enable_tcp_proxy: bool = False,
           idle_timeout: int = 300,
           _experimental_enable_light_sleep: bool = False,
           block_network: bool = False,
           outbound_allowlist: Optional[List[str]] = None,
           api_token: Optional[str] = None,
           host: Optional[str] = None) -> "ServicePool"
```

Create a pool of ``size`` pre-warmed services built from one
definition.

``type`` selects the definition type: WEB, WORKER, or SANDBOX (the
default). SANDBOX pools keep the sandbox auto-wiring (ports 3030/3031
and the sandbox routes); the platform mints their executor secret, and
an explicit ``SANDBOX_SECRET`` in ``env`` wins over minting. WEB and
WORKER pools carry exactly the declared ``ports`` and ``routes`` — no
secret, no auto ports. The docker overrides (``entrypoint``,
``command``, ``args``) apply to every pool type. Mesh stays AUTO:
there is no pool-level mesh option.

<a id="koyeb.sandbox.pool.ServicePool.update"></a>

#### update

```python
def update(size: Optional[int] = None) -> "ServicePool"
```

Resize the pool; returns the updated pool.

<a id="koyeb.sandbox.pool.ServicePool.delete"></a>

#### delete

```python
def delete() -> None
```

Delete the pool (async server-side: it enters DELETING).

<a id="koyeb.sandbox.pool.ServicePool.refresh"></a>

#### refresh

```python
def refresh() -> "ServicePool"
```

Re-fetch the pool's state (ready_count, status) in place.

<a id="koyeb.sandbox.pool.AsyncServicePool"></a>

## AsyncServicePool Objects

```python
class AsyncServicePool()
```

Async twin of :class:`ServicePool`.

<a id="koyeb.sandbox.snapshot"></a>

# koyeb.sandbox.snapshot

Koyeb Sandbox Snapshot - Snapshot functionality for Koyeb sandboxes

<a id="koyeb.sandbox.snapshot.SnapshotType"></a>

## SnapshotType Objects

```python
class SnapshotType(Enum)
```

Types of sandbox snapshots.

<a id="koyeb.sandbox.snapshot.SnapshotStatus"></a>

## SnapshotStatus Objects

```python
class SnapshotStatus(Enum)
```

Status of a sandbox snapshot.

<a id="koyeb.sandbox.snapshot.Snapshot"></a>

## Snapshot Objects

```python
@dataclass
class Snapshot()
```

Represents a sandbox snapshot resource.

A snapshot captures the state of a sandbox at a specific point in time,
including its filesystem and optionally running processes. Sandboxes can
be spawned from snapshots to create pre-configured environments.

<a id="koyeb.sandbox.snapshot.Snapshot.get"></a>

#### get

```python
@classmethod
def get(cls,
        snapshot_id: str,
        api_token: Optional[str] = None,
        host: Optional[str] = None) -> Snapshot
```

Get a snapshot by ID.

Uses the InstanceSnapshots API which is for sandbox/service instance snapshots.

**Arguments**:

- `snapshot_id` - The ID of the snapshot to retrieve
- `api_token` - Koyeb API token (falls back to KOYEB_API_TOKEN env var)
- `host` - Koyeb API host
  

**Returns**:

- `Snapshot` - The snapshot object
  

**Raises**:

- `SandboxError` - If snapshot cannot be retrieved

<a id="koyeb.sandbox.snapshot.Snapshot.list"></a>

#### list

```python
@classmethod
def list(cls,
         service_id: Optional[str] = None,
         snapshot_type: Optional[SnapshotType] = None,
         status: Optional[SnapshotStatus] = None,
         limit: int = 50,
         offset: int = 0,
         api_token: Optional[str] = None,
         host: Optional[str] = None) -> List[Snapshot]
```

List snapshots with optional filters.

Uses the InstanceSnapshots API which is for sandbox/service instance snapshots.

**Arguments**:

- `service_id` - Filter by service ID
- `snapshot_type` - Filter by snapshot type
- `status` - Filter by snapshot status
- `limit` - Maximum number of snapshots to return
- `offset` - Offset for pagination
- `api_token` - Koyeb API token
- `host` - Koyeb API host
  

**Returns**:

  List of Snapshot objects

<a id="koyeb.sandbox.snapshot.Snapshot.refresh"></a>

#### refresh

```python
def refresh() -> None
```

Refresh snapshot state from the API.

<a id="koyeb.sandbox.snapshot.Snapshot.wait_available"></a>

#### wait\_available

```python
def wait_available(timeout: int = 600, poll_interval: float = 5.0) -> bool
```

Wait for snapshot to become available.

**Arguments**:

- `timeout` - Maximum time to wait in seconds
- `poll_interval` - Time between status checks in seconds
  

**Returns**:

  True if snapshot became available, False if timeout

<a id="koyeb.sandbox.snapshot.Snapshot.delete"></a>

#### delete

```python
def delete() -> bool
```

Delete this snapshot.

Uses the InstanceSnapshots API which is for sandbox/service instance snapshots.

**Returns**:

  True if deletion was successful

<a id="koyeb.sandbox.snapshot.Snapshot.spawn"></a>

#### spawn

```python
def spawn(name: Optional[str] = None,
          wait_ready: bool = True,
          timeout: int = 300,
          **create_kwargs) -> Sandbox
```

Spawn a new sandbox from this snapshot.

**Arguments**:

- `name` - Name for the new sandbox
- `wait_ready` - Whether to wait for sandbox to be ready
- `timeout` - Timeout for sandbox creation in seconds
- `**create_kwargs` - Additional arguments to pass to Sandbox.create()
  

**Returns**:

- `Sandbox` - A new sandbox instance initialized from this snapshot

<a id="koyeb.sandbox.snapshot.DeclarativeSnapshot"></a>

## DeclarativeSnapshot Objects

```python
class DeclarativeSnapshot()
```

Fluent builder for creating sandbox snapshots declaratively.

This builder allows you to define a sandbox environment by:
- Writing files
- Copying local files/directories
- Running setup commands
- Setting environment variables

Then builds a snapshot that can be used to spawn pre-configured sandboxes.

<a id="koyeb.sandbox.snapshot.DeclarativeSnapshot.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str,
             image: str,
             workdir: Optional[str] = None,
             api_token: Optional[str] = None,
             host: Optional[str] = None,
             delete_builder: bool = True)
```

Initialize the declarative snapshot builder.

**Arguments**:

- `name` - Name for the template/builder
- `image` - Docker image to use for the sandbox
- `workdir` - Working directory in the sandbox
- `api_token` - Koyeb API token
- `host` - Koyeb API host
- `delete_builder` - Whether to delete the builder sandbox after creating the snapshot (default: True)

<a id="koyeb.sandbox.snapshot.DeclarativeSnapshot.file"></a>

#### file

```python
def file(path: str, content: str) -> DeclarativeSnapshot
```

Write a file to the sandbox during build.

**Arguments**:

- `path` - Path in the sandbox (e.g., "/workspace/requirements.txt")
- `content` - File content as string
  

**Returns**:

  self for method chaining

<a id="koyeb.sandbox.snapshot.DeclarativeSnapshot.copy"></a>

#### copy

```python
def copy(src: str, dst: str) -> DeclarativeSnapshot
```

Copy a local file or directory to the sandbox during build.

**Arguments**:

- `src` - Local source path (file or directory)
- `dst` - Destination path in the sandbox
  

**Returns**:

  self for method chaining

<a id="koyeb.sandbox.snapshot.DeclarativeSnapshot.run"></a>

#### run

```python
def run(command: str, cwd: Optional[str] = None) -> DeclarativeSnapshot
```

Run a command during build.

**Arguments**:

- `command` - Command to execute
- `cwd` - Working directory for the command
  

**Returns**:

  self for method chaining

<a id="koyeb.sandbox.snapshot.DeclarativeSnapshot.build"></a>

#### build

```python
def build(snapshot_name: Optional[str] = None) -> Snapshot
```

Build the snapshot by creating a temporary sandbox,
applying all configurations, and creating a snapshot.

The builder sandbox is automatically deleted after the snapshot is created.

**Arguments**:

- `snapshot_name` - Name for the snapshot (defaults to builder name)
  

**Returns**:

- `Snapshot` - The created snapshot

<a id="koyeb.sandbox.snapshot.DeclarativeSnapshot.get_operations"></a>

#### get\_operations

```python
def get_operations() -> List[str]
```

Get list of operations recorded during build.

<a id="koyeb.sandbox.errors"></a>

# koyeb.sandbox.errors

The SDK error taxonomy: every failure the sandbox layer raises is a
SandboxError subclass, so callers catch one family.

<a id="koyeb.sandbox.errors.SandboxError"></a>

## SandboxError Objects

```python
class SandboxError(Exception)
```

Base exception for sandbox operations

<a id="koyeb.sandbox.errors.MissingApiTokenError"></a>

## MissingApiTokenError Objects

```python
class MissingApiTokenError(SandboxError, ValueError)
```

Raised when no API token is provided and KOYEB_API_TOKEN is unset.

Also inherits ValueError for back-compat with published 1.5.x callers
that catch the old plain ValueError from the token gates.

<a id="koyeb.sandbox.errors.InvalidPortError"></a>

## InvalidPortError Objects

```python
class InvalidPortError(SandboxError, ValueError)
```

Raised when a port is not an integer in [MIN_PORT, MAX_PORT].

Also inherits ValueError for back-compat with published 1.5.x callers
that catch the old plain ValueError from validate_port.

<a id="koyeb.sandbox.errors.NoSandboxSecretError"></a>

## NoSandboxSecretError Objects

```python
class NoSandboxSecretError(SandboxError)
```

Raised when a sandbox deployment carries no SANDBOX_SECRET, so the
executor connection cannot be established.

<a id="koyeb.sandbox.errors.SandboxTimeoutError"></a>

## SandboxTimeoutError Objects

```python
class SandboxTimeoutError(SandboxError)
```

Raised when a sandbox operation times out

<a id="koyeb.sandbox.errors.SandboxDeploymentError"></a>

## SandboxDeploymentError Objects

```python
class SandboxDeploymentError(SandboxError)
```

Raised when a sandbox deployment reaches an error state

<a id="koyeb.sandbox.errors.SandboxRequestError"></a>

## SandboxRequestError Objects

```python
class SandboxRequestError(SandboxError)
```

Raised when the sandbox executor returns a non-OK HTTP response.

Carries the HTTP status code and response body. SandboxServiceError
(HTTP 5xx) subclasses this, so `except SandboxRequestError` catches
every executor HTTP failure — mirroring the JS SDK's SandboxRequestError.

<a id="koyeb.sandbox.errors.SandboxServiceError"></a>

## SandboxServiceError Objects

```python
class SandboxServiceError(SandboxRequestError)
```

Raised when the sandbox executor returns an HTTP 5xx error

<a id="koyeb.sandbox.errors.EgressPolicyError"></a>

## EgressPolicyError Objects

```python
class EgressPolicyError(SandboxError)
```

Raised when egress policy arguments are invalid or conflicting

<a id="koyeb.sandbox.errors.PoolClaimError"></a>

## PoolClaimError Objects

```python
class PoolClaimError(SandboxError)
```

Raised when claiming a sandbox from a service pool fails

<a id="koyeb.sandbox.errors.ServicePoolError"></a>

## ServicePoolError Objects

```python
class ServicePoolError(SandboxError)
```

Raised when a service pool operation fails

<a id="koyeb.sandbox.errors.ServiceTerminalStateError"></a>

## ServiceTerminalStateError Objects

```python
class ServiceTerminalStateError(SandboxError)
```

Raised when a service reaches a state that will never become ready

<a id="koyeb.sandbox.status"></a>

# koyeb.sandbox.status

Status classification for readiness polling, failing closed on
unknown or terminal states.

<a id="koyeb.sandbox.status.classify_service_status"></a>

#### classify\_service\_status

```python
def classify_service_status(
        status: Union[ServiceStatus, str]) -> StatusClassification
```

Classify a service status for readiness, failing closed.

HEALTHY and DEGRADED are usable, STARTING and RESUMING are still in
progress, and every other state — including unknown forward-compat
values — is a terminal failure. Mirrors the JS SDK's
classifyServiceStatus (src/claim.ts).

<a id="koyeb.sandbox.status.classify_deployment_status"></a>

#### classify\_deployment\_status

```python
def classify_deployment_status(
        status: Union[DeploymentStatus, str]) -> StatusClassification
```

Classify a deployment status for readiness, failing closed.

HEALTHY and DEGRADED are ready, the pre-ready states (PENDING,
PROVISIONING, SCHEDULED, ALLOCATING, STARTING) are in progress, and every
other state — including SLEEPING, STASHED, and unknown forward-compat
values — is terminal: it will not become ready on its own during a wait.

<a id="koyeb.sandbox.clients"></a>

# koyeb.sandbox.clients

Control-plane client bundles, their (token, host) caches, and the
sandbox executor client factories.

<a id="koyeb.sandbox.clients.ApiClients"></a>

## ApiClients Objects

```python
@dataclass(frozen=True)
class ApiClients()
```

Bundle of Koyeb API clients sharing a single underlying ApiClient.

<a id="koyeb.sandbox.clients.get_api_clients"></a>

#### get\_api\_clients

```python
def get_api_clients(api_token: Optional[str] = None,
                    host: Optional[str] = None) -> ApiClients
```

Get configured API clients for Koyeb operations.

Caches clients by (token, host) to reuse the underlying HTTP connection pool.

**Arguments**:

- `api_token` - Koyeb API token. If not provided, will try to get from KOYEB_API_TOKEN env var
- `host` - Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)
  

**Returns**:

  ApiClients with apps, services, instances, catalog_instances, deployments, and secrets attributes
  

**Raises**:

- `ValueError` - If API token is not provided

<a id="koyeb.sandbox.clients.AsyncApiClients"></a>

## AsyncApiClients Objects

```python
@dataclass(frozen=True)
class AsyncApiClients()
```

Bundle of async Koyeb API clients sharing a single underlying AsyncApiClient.

<a id="koyeb.sandbox.clients.get_async_api_clients"></a>

#### get\_async\_api\_clients

```python
def get_async_api_clients(api_token: Optional[str] = None,
                          host: Optional[str] = None) -> AsyncApiClients
```

Get configured async API clients for Koyeb operations.

Caches clients by (token, host) to reuse the underlying HTTP connection pool.

**Arguments**:

- `api_token` - Koyeb API token. If not provided, will try to get from KOYEB_API_TOKEN env var
- `host` - Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var
  

**Returns**:

  AsyncApiClients with async API client instances
  

**Raises**:

- `ValueError` - If API token is not provided

<a id="koyeb.sandbox.clients.create_sandbox_client"></a>

#### create\_sandbox\_client

```python
def create_sandbox_client(conn_info: Optional["ConnectionInfo"],
                          existing_client: Optional[Any] = None) -> Any
```

Create or return existing SandboxClient instance with validation.

Helper function to create SandboxClient instances with consistent validation.
Used by Sandbox, SandboxExecutor, and SandboxFilesystem to avoid duplication.

**Arguments**:

- `conn_info` - The information needed to connect to the sandbox executor API
- `existing_client` - Existing client instance to return if not None
  

**Returns**:

- `SandboxClient` - Configured client instance
  

**Raises**:

- `SandboxError` - If sandbox URL or secret is not available

<a id="koyeb.sandbox.clients.create_async_sandbox_client"></a>

#### create\_async\_sandbox\_client

```python
def create_async_sandbox_client(conn_info: Optional["ConnectionInfo"],
                                existing_client: Optional[Any] = None) -> Any
```

Create or return existing AsyncSandboxClient instance with validation.

Helper function to create AsyncSandboxClient instances with consistent validation.
Used by AsyncSandbox to avoid duplication.

**Arguments**:

- `conn_info` - The information needed to connect to the sandbox executor API
- `existing_client` - Existing client instance to return if not None
  

**Returns**:

- `AsyncSandboxClient` - Configured async client instance
  

**Raises**:

- `SandboxError` - If sandbox URL or secret is not available

<a id="koyeb.sandbox.egress"></a>

# koyeb.sandbox.egress

Outbound egress policy building and destination normalization.

<a id="koyeb.sandbox.egress.build_network_policy"></a>

#### build\_network\_policy

```python
def build_network_policy(
        block_network: bool = False,
        outbound_allowlist: Optional[List[str]] = None
) -> Optional[NetworkPolicy]
```

Build a NetworkPolicy from sandbox network policy arguments.

**Arguments**:

- `block_network` - If True, block all outbound network access
- `outbound_allowlist` - List of IPs/CIDRs allowed as outbound
  destinations; all other outbound traffic is blocked. Bare IPs
  are normalized to /32 (IPv4) or /128 (IPv6). An empty list
  blocks all outbound traffic.
  

**Returns**:

  NetworkPolicy, or None when both arguments are unset
  (block_network=False and outbound_allowlist=None)
  

**Raises**:

- `EgressPolicyError` - If both arguments are passed, or an allowlist
  entry is not a valid IP address or CIDR

