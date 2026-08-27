#!/usr/bin/env python3
"""Emit only organizer-permitted HPO identifiers and ontology labels."""

from __future__ import annotations

import json
import os
from pathlib import Path


PRIVATE_DIR = Path("/srv/mva-private")
QC_DETAIL_PATH = PRIVATE_DIR / "private_qc_detail.json"
ONTOLOGY_PATH = Path("/opt/mva-public/hp.obo")
OUTPUT_PATH = PRIVATE_DIR / "hpo_summary_private.json"
SAFE_RECEIPT_PATH = PRIVATE_DIR / "hpo_summary_safe_receipt.json"


def ontology_labels(path: Path, wanted: set[str]) -> dict[str, str]:
    labels: dict[str, str] = {}
    current_id = ""
    current_name = ""
    obsolete = False

    def flush() -> None:
        if current_id in wanted and current_name and not obsolete:
            labels[current_id] = current_name

    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if line == "[Term]":
            flush()
            current_id = ""
            current_name = ""
            obsolete = False
        elif line.startswith("id: HP:"):
            current_id = line.removeprefix("id: ")
        elif line.startswith("name: "):
            current_name = line.removeprefix("name: ")
        elif line == "is_obsolete: true":
            obsolete = True
    flush()
    return labels


def main() -> int:
    os.umask(0o077)
    qc = json.loads(QC_DETAIL_PATH.read_text(encoding="utf-8"))
    hpo_ids = qc.get("hpo_ids")
    if not isinstance(hpo_ids, list) or not 1 <= len(hpo_ids) <= 20:
        raise RuntimeError("Fail closed: HPO summary must contain one to twenty terms")
    wanted = {str(value) for value in hpo_ids}
    labels = ontology_labels(ONTOLOGY_PATH, wanted)
    if set(labels) != wanted:
        raise RuntimeError("Fail closed: one or more HPO labels were not resolved")
    output = [{"id": hpo_id, "label": labels[hpo_id]} for hpo_id in sorted(wanted)]
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    OUTPUT_PATH.chmod(0o600)
    receipt = {
        "status": "PASS",
        "hpo_term_count": len(output),
        "raw_narrative_emitted": False,
        "genome_scale_values_emitted": False,
    }
    SAFE_RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    SAFE_RECEIPT_PATH.chmod(0o600)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
