#!/usr/bin/env python3
"""Working directory for commands"""

import os

from koyeb import Sandbox


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return

    sandbox = None
    try:
        sandbox = Sandbox.create(
            image="koyeb/sandbox",
            name="working-dir",
            wait_ready=True,
            api_token=api_token,
        )

        # Setup: create directory structure
        sandbox.exec("mkdir -p /tmp/my_project/src")
        sandbox.exec("echo 'print(\\\"hello\\\")' > /tmp/my_project/src/main.py")

        # Run command in specific directory
        result = sandbox.exec("pwd", cwd="/tmp/my_project")
        print(result.stdout.strip())

        # List files in working directory
        result = sandbox.exec("ls -la", cwd="/tmp/my_project")
        print(result.stdout.strip())

        # Use relative paths
        result = sandbox.exec("cat src/main.py", cwd="/tmp/my_project")
        print(result.stdout.strip())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    main()
