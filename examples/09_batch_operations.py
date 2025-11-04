#!/usr/bin/env python3
"""Batch file operations"""

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
            name="batch-ops",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Write multiple files at once
        files_to_create = [
            {"path": "/tmp/file1.txt", "content": "Content of file 1"},
            {"path": "/tmp/file2.txt", "content": "Content of file 2"},
            {"path": "/tmp/file3.txt", "content": "Content of file 3"},
        ]

        fs.write_files(files_to_create)
        print("Created 3 files")

        # Verify
        created_files = fs.ls("/tmp")
        batch_files = [f for f in created_files if f.startswith("file")]
        print(f"Files: {batch_files}")

        # Create project structure
        project_files = [
            {"path": "/tmp/project/main.py", "content": "print('Hello')"},
            {"path": "/tmp/project/utils.py", "content": "def helper(): pass"},
            {"path": "/tmp/project/README.md", "content": "# My Project"},
        ]

        fs.mkdir("/tmp/project", recursive=True)
        fs.write_files(project_files)
        print("Created project structure")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    main()
