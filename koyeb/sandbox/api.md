# Sandbox Snapshot API

## API Surface

```python
# Snapshot
class Snapshot:
    @classmethod
    def get(snapshot_id, api_token=None, host=None) -> Snapshot
    @classmethod
    def list(service_id=None, snapshot_type=None, status=None, limit=50, offset=0, api_token=None, host=None) -> List[Snapshot]
    def refresh() -> None
    def wait_available(timeout=600, poll_interval=5.0) -> bool
    def delete() -> bool
    def spawn(name=None, wait_ready=True, timeout=300, **kwargs) -> Sandbox

# DeclarativeSnapshot
class DeclarativeSnapshot:
    def __init__(name, image, workdir=None, api_token=None, host=None, delete_builder=True)
    # Declare build steps.
    def file(path, content) -> DeclarativeSnapshot
    def copy(src, dst) -> DeclarativeSnapshot
    def run(command, cwd=None) -> DeclarativeSnapshot
    # Run the build steps and generate a snapshot.
    def build(snapshot_name=None) -> Snapshot

# Sandbox extensions
class Sandbox:
    def snapshot(name, snapshot_type=SnapshotType.FILESYSTEM, wait_available=True, timeout=600) -> Snapshot
    @staticmethod
    def template(name, image, workdir=None, api_token=None, host=None, delete_builder=True) -> DeclarativeSnapshot
```

## Enums

**SnapshotType**: `FILESYSTEM` | `FULL`
**SnapshotStatus**: `INVALID` | `CREATING` | `UPLOADING` | `AVAILABLE` | `DELETING` | `DELETED` | `FAILED`

## Snapshot

### Fields
`id`, `name`, `service_id`, `snapshot_type`, `status`, `created_at`, `deployment_id`, `available_at`, `size`, `region`, `organization_id`, `project_id`, `messages`, `operations`, `api_token`, `host`, `sandbox_secret`

### Methods
`get(snapshot_id, api_token, host) -> Snapshot`
`list(service_id, snapshot_type, status, limit, offset, api_token, host) -> List[Snapshot]`
`refresh()`
`wait_available(timeout=600, poll_interval=5.0) -> bool`
`delete() -> bool`
`spawn(name, wait_ready=True, timeout=300, **kwargs) -> Sandbox`

## Sandbox

`snapshot(name, snapshot_type=FILESYSTEM, wait_available=True, timeout=600) -> Snapshot`
`template(name, image, workdir=None, api_token=None, host=None, delete_builder=True) -> DeclarativeSnapshot`

## DeclarativeSnapshot

Builder for creating snapshots declaratively.

`file(path, content) -> DeclarativeSnapshot`
`copy(src, dst) -> DeclarativeSnapshot`
`run(command, cwd=None) -> DeclarativeSnapshot`
`build(snapshot_name=None) -> Snapshot` - Returns snapshot with operations list
`get_operations() -> List[str]`

## Examples

### 1. Snapshot & Spawn
```python
from koyeb import Sandbox
sbx = Sandbox.create(image="python:3.12", wait_ready=True)
sbx.exec("pip3 install requests")
snapshot = sbx.snapshot(name="python-with-deps")
sbx2 = snapshot.spawn(name="test-runner", wait_ready=True)
```

### 2. Declarative Builder
```python
from koyeb import Sandbox
snapshot = (
    Sandbox.template("ci-env", image="python:3.12", workdir="/workspace")
    .file("requirements.txt", "pytest\nrequests")
    .run("pip install -r requirements.txt")
    .build(snapshot_name="ci-snapshot")
)
for op in snapshot.operations:
    print(f"  - {op}")
```

### 3. Full Snapshot
```python
from koyeb.sandbox import SnapshotType
snapshot = sbx.snapshot(name="full", snapshot_type=SnapshotType.FULL)
```

### 4. Parallel Spawn
```python
runner1 = snapshot.spawn(name="runner1", wait_ready=False)
runner2 = snapshot.spawn(name="runner2", wait_ready=False)
for runner in [runner1, runner2]:
    runner.wait_ready(timeout=300)
```
