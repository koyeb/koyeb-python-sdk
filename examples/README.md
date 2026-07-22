# Koyeb Sandbox Examples

A collection of examples demonstrating the Koyeb Sandbox SDK capabilities.

## Quick Start

```bash
# Set your API token
export KOYEB_API_TOKEN=your_api_token_here

# Run individual examples
uv run python examples/01_create_sandbox.py
```

## Examples

- **01_create_sandbox.py** - Create and manage sandbox instances
- **02_create_sandbox_with_timing.py** - Create sandbox with timing measurements
- **03_basic_commands.py** - Basic command execution
- **04_streaming_output.py** - Real-time streaming output
- **05_environment_variables.py** - Environment variable configuration
- **06_working_directory.py** - Working directory management
- **07_file_operations.py** - File read/write operations
- **08_directory_operations.py** - Directory management
- **09_binary_files.py** - Binary file handling
- **10_batch_operations.py** - Batch file operations
- **11_upload_download.py** - File upload and download
- **12_file_manipulation.py** - File manipulation operations
- **13_background_processes.py** - Background process management (launch, list, kill)
- **14_expose_port.py** - Port exposure via TCP proxy with HTTP verification
- **15_get_sandbox.py** - Create a sandbox and then retrieve it by ID
- **16_create_sandbox_with_auto_delete_simple.py** - Create a sandbox with auto-delete lifecycle setting
- **17_create_sandbox_with_auto_delete.py** - Create sandboxes with auto-delete lifecycle settings
- **18_create_sandbox_with_existing_app.py** - Create a sandbox in an existing app
- **19_entrypoint_and_command.py** - Create sandboxes with custom entrypoint and command
- **20_config_files.py** - Config files with secrets and interpolation
- **21_egress_policy.py** - Block outbound network access or restrict it to an allowlist
- **22_websockets.py** - WebSocket connections
- **23_snapshot_and_spawn.py** - Create a sandbox, take a snapshot, and spawn from it
- **24_declarative_snapshot_builder.py** - Declarative snapshot building
- **25_full_snapshot_and_spawn.py** - Full snapshots with process state preservation
- **26_snapshot_boot_benchmark.py** - Benchmark snapshot boot times (sync)

## Basic Usage

```python
from koyeb import Sandbox

# Create a sandbox
sandbox = await Sandbox.create(
    image="koyeb/sandbox:slim",
    name="my-sandbox",
    wait_ready=True,
    api_token=api_token,
)

# Execute commands
result = await sandbox.exec("echo 'Hello World'")
print(result.stdout)

# Use filesystem
await sandbox.filesystem.write_file("/tmp/file.txt", "Hello!")
content = await sandbox.filesystem.read_file("/tmp/file.txt")

# Cleanup
await sandbox.delete()
```

## Prerequisites

- Koyeb API token from https://app.koyeb.com/account/api
- Python 3.9+
- `uv` package manager (or `pip`)
