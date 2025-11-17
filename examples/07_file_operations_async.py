#!/usr/bin/env python3
"""Basic file operations (async variant)"""

import asyncio
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
            name="file-ops",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Write file
        content = "Hello, Koyeb Sandbox!\nThis is a test file."
        await fs.write_file("/tmp/hello.txt", content)

        # Read file
        file_info = await fs.read_file("/tmp/hello.txt")
        print(file_info.content)

        # Write Python script
        python_code = "#!/usr/bin/env python3\nprint('Hello from Python!')\n"
        await fs.write_file("/tmp/script.py", python_code)
        await sandbox.exec("chmod +x /tmp/script.py")
        result = await sandbox.exec("/tmp/script.py")
        print(result.stdout.strip())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    asyncio.run(main())
