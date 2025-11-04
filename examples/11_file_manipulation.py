#!/usr/bin/env python3
"""File manipulation operations"""

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
            name="file-manip",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Setup
        fs.write_file("/tmp/file1.txt", "Content of file 1")
        fs.write_file("/tmp/file2.txt", "Content of file 2")
        fs.mkdir("/tmp/test_dir", recursive=True)

        # Rename file
        fs.rename_file("/tmp/file1.txt", "/tmp/renamed_file.txt")
        print(f"Renamed: {fs.exists('/tmp/renamed_file.txt')}")

        # Move file
        fs.move_file("/tmp/file2.txt", "/tmp/test_dir/moved_file.txt")
        print(f"Moved: {fs.exists('/tmp/test_dir/moved_file.txt')}")

        # Copy file (read + write)
        original_content = fs.read_file("/tmp/renamed_file.txt")
        fs.write_file("/tmp/test_dir/copied_file.txt", original_content.content)
        print(f"Copied: {fs.exists('/tmp/test_dir/copied_file.txt')}")

        # Delete file
        fs.rm("/tmp/renamed_file.txt")
        print(f"Deleted: {not fs.exists('/tmp/renamed_file.txt')}")

        # Delete directory
        fs.rm("/tmp/test_dir", recursive=True)
        print(f"Directory deleted: {not fs.exists('/tmp/test_dir')}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    main()
