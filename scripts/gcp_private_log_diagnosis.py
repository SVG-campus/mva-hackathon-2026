#!/usr/bin/env python3
"""Classify a private Exomiser log without emitting log content or values."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


PATTERNS = {
    "out_of_memory": r"OutOfMemoryError|Java heap space",
    "sample_mismatch": r"sample names?.{0,80}(?:match|consistent)",
    "no_sample": r"No sample specified",
    "file_not_found": r"FileNotFoundException|NoSuchFileException|does not exist",
    "vcf_decode": r"TribbleException|VCF.*(?:parse|decode|invalid)",
    "index_problem": r"tabix|\.tbi|\.csi|index.*(?:invalid|missing|not found)",
    "contig_problem": r"contig.*(?:unknown|invalid|not found|mismatch)",
    "data_problem": r"data.*(?:version|directory).*(?:missing|not found|invalid)",
    "phenotype_problem": r"phenotypicFeatures|HPO|phenotype.*(?:missing|invalid|empty)",
    "bean_creation": r"BeanCreationException|UnsatisfiedDependencyException",
    "illegal_argument": r"IllegalArgumentException",
    "null_pointer": r"NullPointerException",
}


def diagnose(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    text = data.decode("utf-8", errors="replace")
    exception_classes = sorted(
        set(
            re.findall(
                r"(?:[A-Za-z_$][\w$]*\.)+[A-Za-z_$][\w$]*(?:Exception|Error)",
                text,
            )
        )
    )
    return {
        "status": "CLASSIFIED",
        "byte_count": len(data),
        "line_count": len(text.splitlines()),
        "sha256": hashlib.sha256(data).hexdigest(),
        "categories": sorted(
            name for name, pattern in PATTERNS.items() if re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        ),
        "exception_classes": exception_classes,
        "content_emitted": False,
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: gcp_private_log_diagnosis.py LOG")
    print(json.dumps(diagnose(Path(sys.argv[1])), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
