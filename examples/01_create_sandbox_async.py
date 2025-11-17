#!/usr/bin/env python3
"""Create and manage a sandbox (async variant)"""

import asyncio
import os

from koyeb import AsyncSandbox


async def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return

    sandbox = None
    try:
        sandbox = await AsyncSandbox.create(
            image="koyeb/sandbox",
            name="example-sandbox",
            wait_ready=True,
            api_token=api_token,
        )

        # Check health
        is_healthy = await sandbox.is_healthy()
        print(f"Healthy: {is_healthy}")

        # Test command
        result = await sandbox.exec("echo 'Sandbox is ready!'")
        print(result.stdout.strip())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    asyncio.run(main())
