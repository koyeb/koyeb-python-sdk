#!/usr/bin/env python3
"""Directory operations"""

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
            name="directory-ops",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Create directory
        fs.mkdir("/tmp/my_project")

        # Create nested directories
        fs.mkdir("/tmp/my_project/src/utils", recursive=True)

        # List directory
        contents = fs.list_dir("/tmp/my_project")
        print(f"Contents: {contents}")

        # Create project structure
        fs.mkdir("/tmp/my_project/src", recursive=True)
        fs.mkdir("/tmp/my_project/tests", recursive=True)
        fs.write_file("/tmp/my_project/src/main.py", "print('Hello')")
        fs.write_file("/tmp/my_project/README.md", "# My Project")

        # Check if path exists
        exists = fs.exists("/tmp/my_project")
        is_dir = fs.is_dir("/tmp/my_project")
        is_file = fs.is_file("/tmp/my_project/src/main.py")
        print(f"Exists: {exists}, Is dir: {is_dir}, Is file: {is_file}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    main()
