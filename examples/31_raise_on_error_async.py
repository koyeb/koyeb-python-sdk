#!/usr/bin/env python3
"""Opt-in exec errors, async variant (raise_on_error)"""

import asyncio
import os
import sys

from koyeb.sandbox import AsyncSandbox, SandboxCommandError


async def main() -> int:
    api_token = os.environ.get("KOYEB_API_TOKEN")
    if not api_token:
        print("KOYEB_API_TOKEN is not set", file=sys.stderr)
        return 1

    sandbox = await AsyncSandbox.create(name="raise-demo", api_token=api_token)
    print(f"✓ Created {sandbox.service_id}")

    try:
        # Default: a failed command is a value, not an exception.
        result = await sandbox.exec("ls /definitely-missing")
        print(f"✓ Default returned success={result.success}, exit={result.exit_code}")

        # Opt-in: the same command raises, with the result attached.
        try:
            await sandbox.exec("ls /definitely-missing", raise_on_error=True)
        except SandboxCommandError as e:
            print(f"✓ Raised SandboxCommandError: exit={e.result.exit_code}")
            print(f"  stderr: {e.result.stderr.strip()}")
        return 0
    finally:
        await sandbox.delete()
        print("✓ Cleaned up")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
