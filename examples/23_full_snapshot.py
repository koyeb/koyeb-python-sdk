#!/usr/bin/env python3
"""Create a sandbox, take a FULL snapshot (including processes), and spawn from it"""

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
            name=f"full-snapshot-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )
        print(f"  ✓ Sandbox created: {sbx.name}")

        # Install packages
        print("✓ Installing packages...")
        sbx.exec("pip3 install requests")
        print("  ✓ Packages installed")

        # Take a FULL snapshot (includes both filesystem and running processes)
        print("✓ Creating FULL snapshot...")
        snapshot = sbx.snapshot(
            name=f"python-full-{suffix}",
            snapshot_type=SnapshotType.FULL,
        )
        print(f"  ✓ Full snapshot created: {snapshot.name}")
        print(f"  ✓ Snapshot type: {snapshot.snapshot_type.value}")
        
        # Print operations if any
        if snapshot.operations:
            print("\n  Operations performed during snapshot:")
            for op in snapshot.operations:
                print(f"    - {op}")

        # Spawn a new sandbox from the full snapshot
        print("✓ Spawning sandbox from FULL snapshot...")
        sbx2 = snapshot.spawn(
            name=f"full-test-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )
        print(f"  ✓ Sandbox spawned from full snapshot: {sbx2.name}")

        # Verify the sandbox is running and packages are pre-installed
        print("✓ Verifying sandbox from full snapshot...")
        result = sbx2.exec("python3 -c \"import requests; print('OK')\"")
        print(f"  ✓ Result: {result.stdout.strip()}")

        print("\n✓ All tests passed!")
        return 0
    finally:
        print("\nCleaning up resources...")
        if sbx2:
            sbx2.delete()
            print("  ✓ Deleted spawned sandbox")
        if snapshot:
            snapshot.delete()
            print("  ✓ Deleted snapshot")
        if sbx:
            sbx.delete()
            print("  ✓ Deleted original sandbox")
        print("  ✓ Cleanup complete")


if __name__ == "__main__":
    sys.exit(main())
