"""Load local environment variables for the example runners."""

import os
import re
from pathlib import Path
from typing import Optional, Union


_ENV_KEY = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def load_env_file(path: Optional[Union[str, Path]] = None) -> bool:
    """Load a simple .env file without replacing existing variables."""
    env_path = (
        Path(path)
        if path is not None
        else Path(__file__).resolve().parents[1] / ".env"
    )

    try:
        lines = env_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return False

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("export "):
            line = line[7:].lstrip()

        if "=" not in line:
            raise ValueError(f"Invalid .env entry at {env_path}:{line_number}")

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not _ENV_KEY.fullmatch(key):
            raise ValueError(f"Invalid .env key at {env_path}:{line_number}")

        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]

        os.environ.setdefault(key, value)

    return True
