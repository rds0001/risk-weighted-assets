#!/usr/bin/env python3
"""Validate the metadata-only regulatory-source boundary.

Copyright (C) 2026 RiskDataScience GmbH.
SPDX-License-Identifier: GPL-3.0-only
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse


HERE = Path(__file__).resolve().parent
STANDARDS = HERE.parent
MANIFEST = HERE / "sources.json"
ALLOWED_FILES = {
    Path("README.md"),
    Path("00_manifest/sources.json"),
    Path("00_manifest/validate_sources.py"),
}
REQUIRED_SOURCE_FIELDS = {
    "source_id",
    "title",
    "issuer",
    "official_url",
    "archival_name",
    "archival_sha256",
    "retrieved_at",
    "redistributed",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate() -> list[str]:
    errors: list[str] = []
    actual_files = {
        path.relative_to(STANDARDS)
        for path in STANDARDS.rglob("*")
        if path.is_file()
    }
    unexpected = sorted(actual_files - ALLOWED_FILES)
    if unexpected:
        errors.append("unexpected redistributed file(s): " + ", ".join(map(str, unexpected)))
    if any(path.is_symlink() for path in STANDARDS.rglob("*")):
        errors.append("symlinks are not permitted under Standards/")

    try:
        payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return errors + [f"cannot read valid sources.json: {exc}"]

    if payload.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if payload.get("distribution_policy") != "metadata-only":
        errors.append("distribution_policy must be metadata-only")
    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        return errors + ["sources must be a non-empty list"]

    identifiers: set[str] = set()
    for index, source in enumerate(sources):
        label = f"sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = REQUIRED_SOURCE_FIELDS - source.keys()
        if missing:
            errors.append(f"{label} missing fields: {', '.join(sorted(missing))}")
        source_id = str(source.get("source_id", ""))
        if not source_id or source_id in identifiers:
            errors.append(f"{label} has an empty or duplicate source_id")
        identifiers.add(source_id)
        parsed = urlparse(str(source.get("official_url", "")))
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{label} official_url must be an absolute HTTPS URL")
        checksum = str(source.get("archival_sha256", ""))
        if not re.fullmatch(r"[0-9a-f]{64}", checksum):
            errors.append(f"{label} archival_sha256 must be lowercase SHA-256")
        if source.get("redistributed") is not False:
            errors.append(f"{label} must declare redistributed=false")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Source inventory valid: metadata-only boundary confirmed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
