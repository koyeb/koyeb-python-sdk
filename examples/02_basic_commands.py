#!/usr/bin/env python3
"""Basic command execution"""

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
            image="python:3.11",
            name="basic-commands",
            wait_ready=True,
            api_token=api_token,
        )

        # Simple command
        result = sandbox.exec("echo 'Hello World'")
        print(result.stdout.strip())

        # Python command
        result = sandbox.exec("python3 -c 'print(2 + 2)'")
        print(result.stdout.strip())

        # Multi-line Python script
        result = sandbox.exec(
            '''python3 -c "
import sys
print(f'Python version: {sys.version.split()[0]}')
print(f'Platform: {sys.platform}')
"'''
        )
        print(result.stdout.strip())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    main()
