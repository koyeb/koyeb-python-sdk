#!/usr/bin/env python3
"""Claim a sandbox from a service pool (sync).

Set KOYEB_POOL_ID (create one with examples/28_service_pool.py first).
claim() is idempotent per (pool_id, request_id): replaying the same pair
returns the same sandbox instead of consuming another.
"""

import os
import sys

from koyeb.sandbox import (
    PoolClaimError,
    Sandbox,
    SandboxError,
    claim,
    wait_claim_ready,
)


def main() -> int:
    api_token = os.getenv("KOYEB_API_TOKEN")
    pool_id = os.getenv("KOYEB_POOL_ID")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1
    if not pool_id:
        print("Error: KOYEB_POOL_ID not set (create a service pool first)")
        return 1

    try:
        # Claim a sandbox from the pool. The request id is generated once
        # and preserved across internal retries.
        print(f"Claiming a sandbox from pool {pool_id}...")
        result = claim(pool_id, api_token=api_token)

        print("✓ Claim fulfilled")
        print(f"  Claim ID:    {result.claim_id}")
        print(f"  Service ID:  {result.service_id}")
        print(f"  Prewarmed:   {result.prewarmed}")
        print(f"  Request ID:  {result.request_id}")

        if not result.prewarmed:
            # Cold path: no warm sandbox was available, so the claimed
            # service was provisioned on demand — wait for it to boot.
            wait_claim_ready(result, api_token=api_token)
            print("✓ Claimed sandbox is ready")

        # Attach to the claimed service and use it like any other sandbox.
        # The pool owns the claimed sandbox's lifecycle — no delete here.
        sandbox = Sandbox.get_from_id(result.service_id, api_token=api_token)
        out = sandbox.exec("echo 'Hello from a claimed sandbox!'")
        print(f"  Output: {out.stdout.strip()}")

        # Replay demo: the same (pool_id, request_id) returns the same claim.
        replay = claim(
            pool_id, request_id=result.request_id, api_token=api_token
        )
        assert replay.service_id == result.service_id
        print("✓ Replay with the same request_id returned the same service")
        return 0
    except PoolClaimError as e:
        # Claim failed (pool missing, terminal state, retries exhausted, ...)
        print(f"Claim failed: {e}")
        return 1
    except SandboxError as e:
        print(f"Sandbox error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
