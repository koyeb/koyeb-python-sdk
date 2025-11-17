#!/usr/bin/env python3
"""Create and manage a sandbox"""

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
            name="example-sandbox",
            wait_ready=True,
            api_token=api_token,
        )

        # Check health
        is_healthy = sandbox.is_healthy()
        print(f"Healthy: {is_healthy}")

        # Test command
        result = sandbox.exec("echo 'Sandbox is ready!'")
        print(result.stdout.strip())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    main()
