#!/usr/bin/env python3
"""Environment variables in commands (async variant)"""

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
            name="env-vars",
            wait_ready=True,
            api_token=api_token,
        )

        # Set environment variables
        env_vars = {"MY_VAR": "Hello", "DEBUG": "true"}
        result = await sandbox.exec("env | grep MY_VAR", env=env_vars)
        print(result.stdout.strip())

        # Use in Python command
        result = await sandbox.exec(
            'python3 -c "import os; print(os.getenv(\'MY_VAR\'))"',
            env={"MY_VAR": "Hello from Python!"},
        )
        print(result.stdout.strip())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    asyncio.run(main())
