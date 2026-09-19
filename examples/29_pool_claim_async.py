#!/usr/bin/env python3
"""Claim a sandbox from a service pool (async variant)"""

import asyncio
import os
import sys

from koyeb import AsyncPoolClaim, AsyncSandbox
from koyeb.sandbox import SandboxClaimError, SandboxError


async def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    pool_id = os.getenv("KOYEB_POOL_ID")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1
    if not pool_id:
        print("Error: KOYEB_POOL_ID not set (create a service pool first)")
        return 1

    try:
        # Claim a sandbox from the pool. The request id is generated once and
        # preserved across internal retries; replaying the same
        # (pool_id, request_id) pair returns the same claim.
        print(f"Claiming a sandbox from pool {pool_id}...")
        claim = await AsyncPoolClaim.claim(
            pool_id=pool_id,
            api_token=api_token,
        )

        print("✓ Claim fulfilled")
        print(f"  Claim ID:    {claim.claim_id}")
        print(f"  Service ID:  {claim.service_id}")
        print(f"  Prewarmed:   {claim.prewarmed}")
        print(f"  Request ID:  {claim.request_id}")

        if not claim.prewarmed:
            # Cold path: no warm sandbox was available, so the claimed service
            # was provisioned on demand. claim(wait_ready=True) already waited
            # for it; for manual control use claim(wait_ready=False) and
            # await claim.wait_ready() yourself.
            print("  (cold path: the service was provisioned on demand)")

        # Attach a Sandbox to the claimed service and use it like any other
        # sandbox. The pool owns the claimed sandbox's lifecycle — no delete
        # here (unlike examples/01).
        sandbox = await AsyncSandbox.get_from_id(
            id=claim.service_id, api_token=api_token
        )
        result = await sandbox.exec("echo 'Hello from a claimed sandbox!'")
        print(f"  Output: {result.stdout.strip()}")

        # Replay demo: the same (pool_id, request_id) returns the same claim
        replay = await AsyncPoolClaim.claim(
            pool_id=pool_id,
            request_id=claim.request_id,
            api_token=api_token,
        )
        assert replay.service_id == claim.service_id
        print("✓ Replay with the same request_id returned the same service")

        return 0
    except SandboxClaimError as e:
        # Claim failed (pool missing, request id collision on another pool,
        # claimed service reached a terminal state, ...)
        print(f"Claim failed: {e}")
        return 1
    except SandboxError as e:
        print(f"Sandbox error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
