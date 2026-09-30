#!/usr/bin/env python3
"""Service pool lifecycle: create, list, update, and delete a pool.

A service pool keeps a target number of warm sandboxes ready so that
claiming (see examples/29_pool_claim.py) hands out a pre-provisioned
service instead of provisioning one on demand.
"""

import os
import sys
import time
import uuid

from koyeb.sandbox import ServicePool


def main() -> int:
    api_token = os.environ.get("KOYEB_API_TOKEN")
    region = os.getenv("KOYEB_SERVICE_POOL_REGION", "nl-north-1")
    if not api_token:
        print("KOYEB_API_TOKEN is not set", file=sys.stderr)
        return 1

    # Use a unique name so concurrent or repeated runs don't collide on the
    # server-side unique (name, workspace) index.
    pool_name = f"my-pool-{uuid.uuid4().hex[:8]}"

    pool = None
    try:
        # Create a pool with one warm sandbox. Definition options mirror
        # Sandbox.create (image, instance_type, env, region, ...).
        pool = ServicePool.create(
            name=pool_name, size=1, region=region, api_token=api_token
        )
        print(f"✓ Created {pool}")
        assert pool.id, "Pool creation returned no id"

        # List every pool the caller can see.
        pools = ServicePool.list(api_token=api_token)
        print(f"✓ Listed {len(pools)} pool(s)")
        assert any(p.id == pool.id for p in pools), "Created pool missing from list"

        deadline = time.time() + 300
        while time.time() < deadline:
            pool.refresh()
            status = getattr(pool.status, "value", pool.status)
            if status == "ERROR":
                raise RuntimeError("Pool entered ERROR before it became ready")
            if pool.ready_count == pool.size:
                break
            time.sleep(2)
        else:
            raise AssertionError("Pool did not become ready within 300 seconds")

        # Update the pool's target size.
        pool.update(size=2)
        print("✓ Updated: size=2")

        # Refresh re-fetches the pool (status, ready_count, ...).
        pool.refresh()
        print(f"✓ Refreshed, ready_count={pool.ready_count}, status={pool.status}")
        assert pool.size == 2, f"Expected size 2 after update, got {pool.size}"
    except Exception as e:  # noqa: BLE001 - surface any failure but still clean up
        print(f"✗ Service pool example failed: {e}", file=sys.stderr)
        return 1
    finally:
        # Delete the pool no matter what. The server fences it until
        # outstanding claims drain.
        if pool is not None:
            try:
                pool.delete()
                print("✓ Deleted")
            except Exception as e:  # noqa: BLE001 - best-effort cleanup
                print(f"⚠ Could not delete pool {pool.id}: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
