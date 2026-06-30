#!/usr/bin/env python3
"""Verify exposed-port security policies: no auth, API key, and Basic Auth.

Follows the same pattern as example 14 (expose_port) and adds a security
policy on the user-facing route so that unauthenticated requests are rejected.
"""

import os
import sys
import time
import random
import string

import httpx

from koyeb import Sandbox
from koyeb.sandbox import ApiKey, BasicAuth

API_KEY = "my-secret-api-key"
BA_USER = "admin"
BA_PASS = "s3cr3t"


def _suffix() -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))


def _setup_server(sandbox: Sandbox) -> str:
    """Write a test file, start an HTTP server on 8080, expose it, return the base URL."""
    sandbox.filesystem.write_file("/tmp/index.html", "<h1>ok</h1>")
    sandbox.launch_process("python3 -m http.server 8080", cwd="/tmp")
    time.sleep(3)

    exposed = sandbox.expose_port(8080)
    print(f"  Exposed at: {exposed.exposed_at}")
    time.sleep(2)
    return exposed.exposed_at


def demo_no_auth(api_token: str) -> None:
    print("\n=== No security policy (public) ===")
    sandbox = None
    try:
        sandbox = Sandbox.create(
            image="koyeb/sandbox:slim",
            name=f"sec-noauth-{_suffix()}",
            api_token=api_token,
        )
        base = _setup_server(sandbox)

        resp = httpx.get(f"{base}/index.html", timeout=15)
        print(f"  GET /index.html  →  {resp.status_code}")
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        print("  ✓ Publicly accessible as expected")
    finally:
        if sandbox:
            sandbox.delete()


def demo_api_key(api_token: str) -> None:
    print("\n=== API key policy ===")
    sandbox = None
    try:
        sandbox = Sandbox.create(
            image="koyeb/sandbox:slim",
            name=f"sec-apikey-{_suffix()}",
            api_token=api_token,
            exposed_port_security_policy=ApiKey(API_KEY),
        )
        base = _setup_server(sandbox)

        # Without key → rejected
        resp = httpx.get(f"{base}/index.html", timeout=15)
        print(f"  GET (no key)             →  {resp.status_code}")
        assert resp.status_code in (401, 403), f"Expected 401/403, got {resp.status_code}"
        print("  ✓ Rejected without key")

        # With correct key → accepted
        resp = httpx.get(
            f"{base}/index.html",
            headers={"x-api-key": f"{API_KEY}"},
            timeout=15,
        )
        print(f"  GET (Bearer {API_KEY})  →  {resp.status_code}")
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        print("  ✓ Accepted with correct API key")
    finally:
        if sandbox:
            sandbox.delete()


def demo_basic_auth(api_token: str) -> None:
    print("\n=== Basic Auth policy ===")
    sandbox = None
    try:
        sandbox = Sandbox.create(
            image="koyeb/sandbox:slim",
            name=f"sec-basicauth-{_suffix()}",
            api_token=api_token,
            exposed_port_security_policy=BasicAuth(username=BA_USER, password=BA_PASS),
        )
        base = _setup_server(sandbox)

        # Without credentials → rejected
        resp = httpx.get(f"{base}/index.html", timeout=15)
        print(f"  GET (no creds)           →  {resp.status_code}")
        assert resp.status_code in (401, 403), f"Expected 401/403, got {resp.status_code}"
        print("  ✓ Rejected without credentials")

        # With correct credentials → accepted
        resp = httpx.get(f"{base}/index.html", auth=(BA_USER, BA_PASS), timeout=15)
        print(f"  GET ({BA_USER}:{BA_PASS})  →  {resp.status_code}")
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        print("  ✓ Accepted with correct Basic Auth credentials")
    finally:
        if sandbox:
            sandbox.delete()


def main() -> int:
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    demo_no_auth(api_token)
    demo_api_key(api_token)
    demo_basic_auth(api_token)
    print("\nAll assertions passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
