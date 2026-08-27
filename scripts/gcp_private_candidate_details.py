#!/usr/bin/env python3
"""Extract bounded pair-level evidence for the organizer-permitted shortlist."""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path


PRIVATE_DIR = Path("/srv/mva-private")
BASELINE_TSV = PRIVATE_DIR / "exomiser-runs" / "baseline_exome" / "baseline_exome.variants.tsv"
SHORTLIST_PATH = PRIVATE_DIR / "candidate_shortlist_private.json"
DETAILS_PATH = PRIVATE_DIR / "candidate_details_private.json"
SAFE_RECEIPT_PATH = PRIVATE_DIR / "candidate_details_safe_receipt.json"

DETAIL_FIELDS = [
    "RANK",
    "GENE_SYMBOL",
    "MOI",
    "EXOMISER_GENE_COMBINED_SCORE",
    "EXOMISER_GENE_PHENO_SCORE",
    "EXOMISER_GENE_VARIANT_SCORE",
    "EXOMISER_VARIANT_SCORE",
    "CONTRIBUTING_VARIANT",
    "CONTIG",
    "START",
    "REF",
    "ALT",
    "QUAL",
    "FILTER",
    "GENOTYPE",
    "FUNCTIONAL_CLASS",
    "HGVS",
    "RS_ID",
    "EXOMISER_ACMG_CLASSIFICATION",
    "EXOMISER_ACMG_EVIDENCE",
    "EXOMISER_ACMG_DISEASE_ID",
    "EXOMISER_ACMG_DISEASE_NAME",
    "CLINVAR_PRIMARY_INTERPRETATION",
    "CLINVAR_STAR_RATING",
    "MAX_FREQ_SOURCE",
    "MAX_FREQ",
    "MAX_PATH_SOURCE",
    "MAX_PATH",
]


def _chrom(value: str) -> str:
    return value if value.startswith("chr") else f"chr{value}"


def extract_details(tsv_path: Path, shortlist: list[dict[str, object]]) -> list[dict[str, object]]:
    if len(shortlist) > 10:
        raise RuntimeError("Fail closed: shortlist exceeds ten candidates")
    wanted: dict[tuple[str, int, str, str], tuple[int, str]] = {}
    for shortlist_rank, candidate in enumerate(shortlist, start=1):
        gene = str(candidate["gene"])
        variants = candidate["variants"]
        if not isinstance(variants, list) or len(variants) != 2:
            raise RuntimeError("Fail closed: candidate is not an exact pair")
        for variant in variants:
            if not isinstance(variant, dict):
                raise RuntimeError("Fail closed: malformed candidate variant")
            key = (
                str(variant["chrom"]),
                int(variant["pos"]),
                str(variant["ref"]),
                str(variant["alt"]),
            )
            wanted[key] = (shortlist_rank, gene)

    evidence: dict[int, dict[str, object]] = {
        rank: {"shortlist_rank": rank, "gene": str(candidate["gene"]), "variants": []}
        for rank, candidate in enumerate(shortlist, start=1)
    }
    with tsv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames:
            reader.fieldnames = [name.lstrip("#") for name in reader.fieldnames]
        for row in reader:
            if (row.get("MOI") or "").strip().upper() != "AR":
                continue
            key = (
                _chrom((row.get("CONTIG") or "").strip()),
                int((row.get("START") or "0").strip()),
                (row.get("REF") or "").strip().upper(),
                (row.get("ALT") or "").strip().upper(),
            )
            match = wanted.get(key)
            if not match:
                continue
            shortlist_rank, gene = match
            if (row.get("GENE_SYMBOL") or "").strip().upper() != gene.upper():
                continue
            detail = {field.lower(): (row.get(field) or "").strip() for field in DETAIL_FIELDS}
            detail["contig"] = key[0]
            evidence[shortlist_rank]["variants"].append(detail)  # type: ignore[union-attr]

    output = [evidence[rank] for rank in sorted(evidence)]
    for candidate in output:
        variants = candidate["variants"]
        if not isinstance(variants, list) or len(variants) != 2:
            raise RuntimeError("Fail closed: expected two evidence rows per candidate")
        variants.sort(key=lambda row: (row["contig"], int(row["start"])))
    return output


def main() -> int:
    os.umask(0o077)
    shortlist = json.loads(SHORTLIST_PATH.read_text(encoding="utf-8"))
    details = extract_details(BASELINE_TSV, shortlist)
    DETAILS_PATH.write_text(json.dumps(details, indent=2) + "\n", encoding="utf-8")
    DETAILS_PATH.chmod(0o600)
    receipt = {
        "status": "PASS",
        "candidate_count": len(details),
        "variant_count": sum(len(candidate["variants"]) for candidate in details),
        "all_candidates_are_pairs": all(len(candidate["variants"]) == 2 for candidate in details),
        "genome_scale_values_emitted": False,
    }
    SAFE_RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    SAFE_RECEIPT_PATH.chmod(0o600)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
