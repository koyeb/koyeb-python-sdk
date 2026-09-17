from datetime import datetime
from unittest.mock import patch

from koyeb.sandbox.sandbox import Sandbox
from koyeb.sandbox.snapshot import Snapshot, SnapshotStatus, SnapshotType


@patch.object(Sandbox, "create")
def test_spawn_preserves_snapshot_project(mock_create):
    snapshot = Snapshot(
        id="snapshot-id",
        name="snapshot",
        service_id="service-id",
        snapshot_type=SnapshotType.FILESYSTEM,
        status=SnapshotStatus.AVAILABLE,
        created_at=datetime.now(),
        project_id="project-id",
        api_token="token",
        sandbox_secret="secret",
    )

    snapshot.spawn(name="restored")

    assert mock_create.call_args.kwargs["project_id"] == "project-id"
