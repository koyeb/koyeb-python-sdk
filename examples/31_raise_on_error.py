#!/usr/bin/env python3
"""Opt-in exec errors: raise_on_error turns a failed command into an exception.

By default a failed command returns a failed CommandResult; with
raise_on_error=True it raises SandboxCommandError carrying the result.
"""

import os
import sys

from koyeb.sandbox import Sandbox, SandboxCommandError


def main() -> int:
    api_token = os.environ.get("KOYEB_API_TOKEN")
    if not api_token:
        print("KOYEB_API_TOKEN is not set", file=sys.stderr)
        return 1

    sandbox = Sandbox.create(name="raise-demo", api_token=api_token)
    print(f"✓ Created {sandbox.service_id}")

    try:
        # Default: a failed command is a value, not an exception.
        result = sandbox.exec("ls /definitely-missing")
        print(f"✓ Default returned success={result.success}, exit={result.exit_code}")

        # Opt-in: the same command raises, with the result attached.
        try:
            sandbox.exec("ls /definitely-missing", raise_on_error=True)
        except SandboxCommandError as e:
            print(f"✓ Raised SandboxCommandError: exit={e.result.exit_code}")
            print(f"  stderr: {e.result.stderr.strip()}")
        return 0
    finally:
        sandbox.delete()
        print("✓ Cleaned up")


if __name__ == "__main__":
    sys.exit(main())
