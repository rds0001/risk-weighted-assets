#!/usr/bin/env python3
"""Build or verify the repository SHA-256 manifest.

Copyright (C) 2026 RiskDataScience GmbH.
SPDX-License-Identifier: GPL-3.0-only
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"
EXCLUDED_PARTS = {
    ".git",
    ".cache",
    ".pytest_cache",
    ".hypothesis",
    "__pycache__",
    ".venv",
    "venv",
    ".tox",
    ".nox",
}


def is_runtime_artifact(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    return (
        bool(EXCLUDED_PARTS.intersection(parts))
        or any(part.endswith(".egg-info") for part in parts)
        or path.name.endswith((".pyc", ".pyo"))
    )


def included_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and path != MANIFEST
        and not is_runtime_artifact(path)
    )


def render() -> str:
    lines = []
    for path in included_files():
        digest = sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify instead of rewriting")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not MANIFEST.is_file():
            print("ERROR: MANIFEST.sha256 is missing", file=sys.stderr)
            return 1
        if MANIFEST.read_text(encoding="utf-8") != expected:
            print("ERROR: MANIFEST.sha256 is stale", file=sys.stderr)
            return 1
        print(f"Manifest valid: {len(included_files())} files verified.")
        return 0
    MANIFEST.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Wrote {MANIFEST.name}: {len(included_files())} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
