#!/usr/bin/env python3
"""Streaming command output"""

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
            name="streaming",
            wait_ready=True,
            api_token=api_token,
        )

        # Stream output in real-time
        result = sandbox.exec(
            '''python3 -c "
import time
for i in range(5):
    print(f'Line {i+1}')
    time.sleep(0.5)
"''',
            on_stdout=lambda data: print(data.strip(), end=" "),
            on_stderr=lambda data: print(f"ERR: {data.strip()}"),
        )
        print(f"\nExit code: {result.exit_code}")

        # Stream a script
        sandbox.filesystem.write_file(
            "/tmp/counter.py",
            "#!/usr/bin/env python3\nimport time\nfor i in range(1, 6):\n    print(f'Count: {i}')\n    time.sleep(0.3)\nprint('Done!')\n",
        )
        sandbox.exec("chmod +x /tmp/counter.py")

        result = sandbox.exec(
            "python3 /tmp/counter.py",
            on_stdout=lambda data: print(data.strip()),
        )

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    main()
