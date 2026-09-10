"""Lesen externer, versionierter Konfigurationsdaten.

Dieses Modul kennt nur Dateiformate und Pflichtfelder. Fachwerte stehen in
YAML bzw. in den daraus erzeugten kanonischen Excel-Tabellen.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


# Repository root. The engine itself lives below ``code/``; all business and
# regulatory data remain in the sibling directory ``daten/``.
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ConfigurationError(ValueError):
    """Konfiguration ist unvollständig oder widersprüchlich."""


def load_yaml(path: Path) -> dict[str, Any]:
    resolved = path if path.is_absolute() else PROJECT_ROOT / path
    if not resolved.is_file():
        raise ConfigurationError(f"Konfigurationsdatei fehlt: {resolved}")
    with resolved.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ConfigurationError(f"Konfigurationswurzel muss ein Objekt sein: {resolved}")
    return value


def load_profile(profile_id: str, config_root: Path | None = None) -> dict[str, Any]:
    root = config_root or PROJECT_ROOT / "daten" / "konfiguration" / "profiles"
    profile = load_yaml(root / f"{profile_id}.yaml")
    required = {"profile_id", "profile_version", "base_as_of_date", "source_inputs", "regulatory_config"}
    missing = sorted(required - set(profile))
    if missing:
        raise ConfigurationError(f"Bankprofil {profile_id}: Pflichtfelder fehlen: {', '.join(missing)}")
    if str(profile["profile_id"]) != profile_id:
        raise ConfigurationError(f"Profil-ID in Datei stimmt nicht mit {profile_id} überein")
    return profile


def load_regulatory_config(path: str | Path) -> dict[str, Any]:
    config = load_yaml(Path(path))
    if not isinstance(config.get("metadata"), dict) or not isinstance(config.get("parameters"), list):
        raise ConfigurationError("Regelkonfiguration benötigt metadata und parameters")
    return config


def regulatory_parameter_items(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Expandiert kompakte zweidimensionale Regeltabellen in Long-Format."""
    items=list(config["parameters"])
    for table in config.get("parameter_tables",[]):
        rows=list(table["rows"]);columns=list(table["columns"]);values=list(table["values"])
        if len(values)!=len(rows) or any(len(line)!=len(columns) for line in values):
            raise ConfigurationError(f"Ungültige Parametermatrix: {table.get('key')}")
        for row_name,line in zip(rows,values):
            for column_name,value in zip(columns,line):
                items.append({"key":table["key"],"d1":str(row_name),"d2":str(column_name),
                              "value":value,"unit":table["unit"],"ref":table["ref"]})
    return items
