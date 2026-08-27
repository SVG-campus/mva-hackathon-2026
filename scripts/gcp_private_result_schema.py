#!/usr/bin/env python3
"""Describe Exomiser result structure without emitting patient-derived values."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RUN_DIR = Path("/srv/mva-private/exomiser-runs")
SAFE_SCHEMA_PATH = Path("/srv/mva-private/result_schema_safe.json")


def first_json_value(path: Path) -> Any:
    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    return json.loads(line)
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def schema(value: Any, depth: int = 0) -> Any:
    if depth >= 6:
        return type(value).__name__
    if isinstance(value, dict):
        return {key: schema(value[key], depth + 1) for key in sorted(value)}
    if isinstance(value, list):
        return [schema(value[0], depth + 1)] if value else []
    return type(value).__name__


def main() -> int:
    receipt: dict[str, object] = {"status": "PASS", "cases": {}}
    for case_dir in sorted(path for path in RUN_DIR.iterdir() if path.is_dir()):
        json_files = sorted(
            path for path in case_dir.iterdir() if path.suffix.lower() in {".json", ".jsonl"}
        )
        case_schema: dict[str, object] = {}
        for path in json_files:
            case_schema[path.suffix.lower()] = schema(first_json_value(path))
        receipt["cases"][case_dir.name] = case_schema  # type: ignore[index]
    SAFE_SCHEMA_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    SAFE_SCHEMA_PATH.chmod(0o600)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
