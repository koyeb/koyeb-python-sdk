#!/usr/bin/env python3
"""Service pool lifecycle: create, list, update, and delete a pool.

A service pool keeps a target number of warm sandboxes ready so that
claiming (see examples/29_pool_claim.py) hands out a pre-provisioned
service instead of provisioning one on demand.
"""

import os
import sys

from koyeb.sandbox import ServicePool


def main() -> int:
    api_token = os.environ.get("KOYEB_API_TOKEN")
    if not api_token:
        print("KOYEB_API_TOKEN is not set", file=sys.stderr)
        return 1

    # Create a pool of 3 warm sandboxes. Definition options mirror
    # Sandbox.create (image, instance_type, env, region, ...).
    pool = ServicePool.create(name="my-pool", size=3, api_token=api_token)
    print(f"✓ Created {pool}")

    # List every pool the caller can see.
    pools = ServicePool.list(api_token=api_token)
    print(f"✓ Listed {len(pools)} pool(s)")

    # Update the pool's target size.
    pool.update(size=5)
    print("✓ Updated: size=5")

    # Refresh re-fetches the pool (status, ready_count, ...).
    pool.refresh()
    print(f"✓ Refreshed, ready_count={pool.ready_count}, status={pool.status}")

    # Delete the pool. The server fences it until outstanding claims drain.
    pool.delete()
    print("✓ Deleted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
