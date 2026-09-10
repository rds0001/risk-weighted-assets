#!/usr/bin/env python3
"""Validate the public RWA repository boundary and reference artifacts.

Copyright (C) 2026 RiskDataScience GmbH.
SPDX-License-Identifier: GPL-3.0-only
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md",
    "LICENSE",
    "NOTICE",
    "DISCLAIMER.md",
    "THIRD_PARTY_NOTICES.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "SUPPORT.md",
    "code/pyproject.toml",
    "code/rwa",
    "Webapp/rwa-web",
    "Standards/README.md",
    "Standards/00_manifest/sources.json",
    "docs/REGULATORY_SOURCES.md",
    ".github/workflows/ci.yml",
}
FORBIDDEN_SUFFIXES = {".pdf", ".doc", ".docx", ".odt", ".rtf"}
TEXT_SUFFIXES = {"", ".md", ".txt", ".py", ".toml", ".yaml", ".yml", ".json", ".cff"}
DATASETS = (
    ROOT / "daten/rechenlaeufe/2026-08-31/v1.0.0",
    ROOT / "daten/rechenlaeufe/2026-08-31/v1.0.0-ksa",
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def validate_dataset(dataset: Path, errors: list[str]) -> None:
    manifest_path = dataset / "dataset_manifest.json"
    if not manifest_path.is_file():
        errors.append(f"missing dataset manifest: {manifest_path.relative_to(ROOT)}")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid dataset manifest {manifest_path.relative_to(ROOT)}: {exc}")
        return
    inputs = sorted((dataset / "inputs").glob("*.xlsx"))
    if len(inputs) != 16:
        errors.append(f"{dataset.relative_to(ROOT)} must contain exactly 16 input workbooks")
    listed = manifest.get("input_workbooks", [])
    if sorted(path.name for path in inputs) != sorted(listed):
        errors.append(f"input inventory mismatch: {dataset.relative_to(ROOT)}")
    hashes = manifest.get("input_sha256", {})
    for path in inputs:
        if hashes.get(path.name) != digest(path):
            errors.append(f"input hash mismatch: {path.relative_to(ROOT)}")

    runs = sorted((dataset / "outputs").glob("RUN-*/run_manifest.json"))
    if len(runs) != 1:
        errors.append(f"{dataset.relative_to(ROOT)} must retain exactly one reference run")
        return
    try:
        run = json.loads(runs[0].read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid run manifest {runs[0].relative_to(ROOT)}: {exc}")
        return
    if run.get("status") != "CALCULATED":
        errors.append(f"reference run is not CALCULATED: {runs[0].relative_to(ROOT)}")
    if run.get("control_count") != 12 or run.get("controls_passed") != 12:
        errors.append(f"reference run controls are not 12/12: {runs[0].relative_to(ROOT)}")
    outputs = sorted(runs[0].parent.glob("*.xlsx"))
    if len(outputs) != 6:
        errors.append(f"reference run must contain exactly six outputs: {runs[0].parent.relative_to(ROOT)}")
    if sorted(path.name for path in outputs) != sorted(run.get("output_files", [])):
        errors.append(f"output inventory mismatch: {runs[0].relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    missing = sorted(path for path in REQUIRED if not (ROOT / path).is_file())
    if missing:
        errors.append("missing required files: " + ", ".join(missing))

    all_paths = list(ROOT.rglob("*"))
    symlinks = [path.relative_to(ROOT) for path in all_paths if path.is_symlink()]
    if symlinks:
        errors.append("symlinks are not permitted: " + ", ".join(map(str, symlinks)))
    prohibited = [
        path.relative_to(ROOT)
        for path in all_paths
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES
    ]
    if prohibited:
        errors.append("downloaded/office documents found: " + ", ".join(map(str, prohibited)))
    factory_name = "scaf" + "fold"
    forbidden_dirs = [
        path.relative_to(ROOT)
        for path in all_paths
        if path.is_dir() and path.name.lower() in {factory_name, "regularien"}
    ]
    if forbidden_dirs:
        errors.append("non-public source directory found: " + ", ".join(map(str, forbidden_dirs)))
    oversized = [
        path.relative_to(ROOT)
        for path in all_paths
        if path.is_file() and path.stat().st_size > 25 * 1024 * 1024
    ]
    if oversized:
        errors.append("file larger than 25 MiB: " + ", ".join(map(str, oversized)))

    absolute_path = re.compile(
        r"(?:/" + "home/|/" + "mnt/|[A-Za-z]:\\\\" + "Users\\\\)"
    )
    secret = re.compile(r"(?:ghp_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)")
    for path in all_paths:
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            value = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(ROOT)
        if absolute_path.search(value):
            errors.append(f"private absolute path found: {rel}")
        if factory_name in value.lower():
            errors.append(f"internal factory term found: {rel}")
        if secret.search(value):
            errors.append(f"credential-like material found: {rel}")
        if "Apache " + "License" in value or "Apache" + "-2.0" in value:
            errors.append(f"unexpected Apache project-license reference: {rel}")

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").is_file() else ""
    if "GNU GENERAL PUBLIC LICENSE" not in license_text or "Version 3" not in license_text:
        errors.append("LICENSE is not the expected GNU GPL version 3 text")
    pyproject = (ROOT / "code/pyproject.toml").read_text(encoding="utf-8") if (ROOT / "code/pyproject.toml").is_file() else ""
    for marker in ("RiskDataScience GmbH", "riskdatascience@web.de", "GPL-3.0-only"):
        if marker not in pyproject:
            errors.append(f"pyproject.toml missing metadata: {marker}")

    for dataset in DATASETS:
        validate_dataset(dataset, errors)

    source_inventory = ROOT / "Standards/00_manifest/sources.json"
    if source_inventory.is_file():
        try:
            sources = json.loads(source_inventory.read_text(encoding="utf-8")).get("sources", [])
            if len(sources) != 2 or any(item.get("redistributed") is not False for item in sources):
                errors.append("source inventory must contain two non-redistributed provenance records")
        except json.JSONDecodeError as exc:
            errors.append(f"invalid source inventory: {exc}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    file_count = sum(path.is_file() for path in all_paths)
    size = sum(path.stat().st_size for path in all_paths if path.is_file())
    print(f"Release boundary valid: {file_count} files, {size / (1024 * 1024):.1f} MiB.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
