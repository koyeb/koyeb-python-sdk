#!/usr/bin/env python3
"""Upload and download files"""

import os
import tempfile

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
            name="upload-download",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Upload local file to sandbox
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("This is a local file\n")
            f.write("Uploaded to Koyeb Sandbox!")
            local_file = f.name

        try:
            fs.upload_file(local_file, "/tmp/uploaded_file.txt")
            uploaded_info = fs.read_file("/tmp/uploaded_file.txt")
            print(uploaded_info.content)
        finally:
            os.unlink(local_file)

        # Download file from sandbox
        fs.write_file(
            "/tmp/download_source.txt", "Download test content\nMultiple lines"
        )

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix="_downloaded.txt") as f:
            download_path = f.name

        try:
            fs.download_file("/tmp/download_source.txt", download_path)
            with open(download_path, "r") as f:
                print(f.read())
        finally:
            os.unlink(download_path)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    main()
