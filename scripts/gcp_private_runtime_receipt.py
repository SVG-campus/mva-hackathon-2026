#!/usr/bin/env python3
"""Emit aggregate runtime/storage evidence without private filenames or content."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


PRIVATE_DIR = Path("/srv/mva-private")
RUN_DIR = PRIVATE_DIR / "exomiser-runs"
OUTPUT_PATH = PRIVATE_DIR / "runtime_safe_receipt.json"
ROUTES = (
    "baseline_exome",
    "challenger_introns",
    "phenotype_ablation",
    "phenotype_shuffle",
)


def _birth_epoch(path: Path) -> int:
    result = subprocess.run(
        ["stat", "-c", "%W", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip().isdigit():
        raise RuntimeError("Fail closed: route start time is unavailable")
    value = int(result.stdout.strip())
    if value <= 0:
        raise RuntimeError("Fail closed: filesystem birth time is unavailable")
    return value


def _directory_bytes(path: Path) -> int:
    result = subprocess.run(
        ["du", "-sb", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("Fail closed: aggregate directory size is unavailable")
    return int(result.stdout.split()[0])


def main() -> int:
    os.umask(0o077)
    runtimes: dict[str, int] = {}
    for route in ROUTES:
        log_path = RUN_DIR / f"{route}.log"
        runtimes[route] = max(0, round(log_path.stat().st_mtime - _birth_epoch(log_path)))
    disk = shutil.disk_usage("/")
    receipt = {
        "status": "PASS",
        "successful_route_runtime_seconds": runtimes,
        "successful_route_runtime_seconds_total": sum(runtimes.values()),
        "public_toolchain_bytes_current": _directory_bytes(Path("/opt/mva-public")),
        "private_workspace_bytes_current": _directory_bytes(PRIVATE_DIR),
        "root_disk_bytes_current_used": disk.used,
        "root_disk_bytes_capacity": disk.total,
        "storage_values_are_current_not_peak": True,
        "raw_narrative_emitted": False,
        "genome_scale_values_emitted": False,
    }
    OUTPUT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    OUTPUT_PATH.chmod(0o600)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
