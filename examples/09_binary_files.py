#!/usr/bin/env python3
"""Binary file operations"""

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
            name="binary-files",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Write binary data (encoding="base64" handles the encoding automatically)
        binary_data = b"Binary data: \x00\x01\x02\x03\xff\xfe\xfd"
        fs.write_file("/tmp/binary.bin", binary_data, encoding="base64")

        # Read binary data (encoding="base64" decodes and returns bytes)
        file_info = fs.read_file("/tmp/binary.bin", encoding="base64")
        print(f"Original: {binary_data}")
        print(f"Read back: {file_info.content}")
        assert binary_data == file_info.content

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    main()
