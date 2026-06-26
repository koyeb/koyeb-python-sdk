#!/usr/bin/env python3
"""Create a sandbox, take a snapshot, and spawn a new sandbox from it"""

import os
import sys
import random
import string

from koyeb import Sandbox
from koyeb.sandbox import SnapshotType


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    sbx = None
    sbx2 = None
    snapshot = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    try:
        print("✓ Creating sandbox...")
        sbx = Sandbox.create(
            image="python:3.12",
            name=f"snapshot-and-spawn-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )
        print(f"  ✓ Sandbox created: {sbx.name}")

        # Install packages
        print("✓ Installing packages...")
        sbx.exec("pip3 install pytest requests")
        print("  ✓ Packages installed")

        # Take a snapshot
        print("✓ Creating snapshot...")
        snapshot = sbx.snapshot(
            name=f"python-with-deps-{suffix}",
            snapshot_type=SnapshotType.FILESYSTEM,
        )
        print(f"  ✓ Snapshot created: {snapshot.name}")

        # Spawn a new sandbox from the snapshot
        print("✓ Spawning sandbox from snapshot...")
        sbx2 = snapshot.spawn(
            name=f"test-runner-{suffix}",
            wait_ready=False,
            api_token=api_token,
        )
        print(f"  ✓ Sandbox spawned: {sbx2.name}")

        # Wait for the spawned sandbox to be ready
        print("✓ Waiting for spawned sandbox to be ready...")
        is_ready = sbx2.wait_ready(timeout=300)
        print("  ✓ Sandbox is ready")

        # Verify packages are pre-installed from snapshot filesystem
        print("✓ Verifying packages are pre-installed from snapshot filesystem...")
        result = sbx2.exec("python3 -c \"import requests; print('OK')\"")
        print(f"  ✓ Result: {result.stdout.strip()}")

        return 0
    finally:
        if sbx2:
            sbx2.delete()
        if snapshot:
            snapshot.delete()
        if sbx:
            sbx.delete()


if __name__ == "__main__":
    sys.exit(main())
