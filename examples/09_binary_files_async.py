#!/usr/bin/env python3
"""Binary file operations (async variant)"""

import asyncio
import base64
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
            name="binary-files",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Write binary data
        binary_data = b"Binary data: \x00\x01\x02\x03\xff\xfe\xfd"
        base64_data = base64.b64encode(binary_data).decode("utf-8")
        await fs.write_file("/tmp/binary.bin", base64_data, encoding="base64")

        # Read binary data
        file_info = await fs.read_file("/tmp/binary.bin", encoding="base64")
        decoded = base64.b64decode(file_info.content)
        print(f"Original: {binary_data}")
        print(f"Decoded: {decoded}")
        assert binary_data == decoded

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    asyncio.run(main())
