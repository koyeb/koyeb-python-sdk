#!/usr/bin/env python3
"""Basic command execution"""

import os, time

from koyeb import Sandbox


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return

    sandbox = None
    try:
        sandbox = Sandbox.create(
            image="python:3.12-alpine3.20",
            name="example-sandbox",
            region="k8s",
            wait_ready=False,
            api_token=api_token,
        )

        print(f"Sandbox URL: {sandbox._get_sandbox_url()}")        

        sandbox.wait_ready()
        
        # Simple command
        result = sandbox.exec("echo 'Hello World'")
        print(f"stdout: {result.stdout.strip()!r}")
        print(f"stderr: {result.stderr.strip()!r}")
        print(f"exit_code: {result.exit_code}")

        # Python command
        for i in range(10):
            result = sandbox.exec(f"python3 -c 'print(\"{i}: 2 + {i} =\", 2 + {i})'")
            print(result.stdout.strip())

            time.sleep(1)
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
