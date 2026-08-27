#!/usr/bin/env python3
"""Emit bounded VCF evidence for only the leading shortlisted variant pair."""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path


PRIVATE_DIR = Path("/srv/mva-private")
MANIFEST_PATH = PRIVATE_DIR / "private_manifest.json"
DETAILS_PATH = PRIVATE_DIR / "candidate_details_private.json"
OUTPUT_PATH = PRIVATE_DIR / "top_pair_vcf_evidence_private.json"
SAFE_RECEIPT_PATH = PRIVATE_DIR / "top_pair_vcf_evidence_safe_receipt.json"
ALLOWED_FORMAT_FIELDS = ("GT", "DP", "GQ", "AD", "PS", "PID", "PGT")


def _contigs(header: str) -> set[str]:
    return set(re.findall(r"^##contig=<ID=([^,>]+)", header, flags=re.MULTILINE))


def _vcf_contig(candidate_contig: str, available: set[str]) -> str:
    candidates = [candidate_contig]
    if candidate_contig.startswith("chr"):
        candidates.append(candidate_contig.removeprefix("chr"))
    else:
        candidates.append(f"chr{candidate_contig}")
    for value in candidates:
        if value in available:
            return value
    raise RuntimeError("Fail closed: shortlisted contig is absent from the VCF header")


def _parse_row(raw: str, expected: dict[str, str]) -> dict[str, object] | None:
    fields = raw.rstrip("\n").split("\t")
    if len(fields) < 10:
        raise RuntimeError("Fail closed: malformed VCF record")
    chrom, pos, _record_id, ref, alt, qual, filt, _info, fmt, sample = fields[:10]
    if (
        int(pos) != int(expected["start"])
        or ref.upper() != expected["ref"].upper()
        or expected["alt"].upper() not in {item.upper() for item in alt.split(",")}
    ):
        return None
    keys = fmt.split(":")
    values = sample.split(":")
    sample_fields = dict(zip(keys, values, strict=False))
    return {
        "chrom": chrom if chrom.startswith("chr") else f"chr{chrom}",
        "pos": int(pos),
        "ref": ref,
        "alt": expected["alt"],
        "qual": qual,
        "filter": filt,
        "format": {
            key: sample_fields[key]
            for key in ALLOWED_FORMAT_FIELDS
            if key in sample_fields and sample_fields[key] not in {"", "."}
        },
    }


def main() -> int:
    os.umask(0o077)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    vcf = Path(manifest["local_files"]["variant"])
    details = json.loads(DETAILS_PATH.read_text(encoding="utf-8"))
    if not isinstance(details, list) or not details:
        raise RuntimeError("Fail closed: candidate details are unavailable")
    lead = details[0]
    variants = lead.get("variants")
    if not isinstance(variants, list) or len(variants) != 2:
        raise RuntimeError("Fail closed: leading candidate is not an exact pair")

    header_result = subprocess.run(
        ["bcftools", "view", "--header-only", str(vcf)],
        check=False,
        capture_output=True,
        text=True,
    )
    if header_result.returncode != 0:
        raise RuntimeError("Fail closed: VCF header read failed")
    available = _contigs(header_result.stdout)

    evidence: list[dict[str, object]] = []
    for expected in variants:
        contig = _vcf_contig(str(expected["contig"]), available)
        region = f"{contig}:{expected['start']}-{expected['start']}"
        result = subprocess.run(
            ["bcftools", "view", "--no-header", "--regions", region, str(vcf)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError("Fail closed: bounded VCF query failed")
        matches = [
            parsed
            for line in result.stdout.splitlines()
            if (parsed := _parse_row(line, expected)) is not None
        ]
        if len(matches) != 1:
            raise RuntimeError("Fail closed: expected exactly one matching VCF record")
        evidence.append(matches[0])

    output = {
        "shortlist_rank": 1,
        "gene": str(lead["gene"]),
        "variants": evidence,
        "phase_interpretation": (
            "phase_set_reported"
            if all(any(key in item["format"] for key in ("PS", "PID", "PGT")) for item in evidence)
            else "trans_not_established"
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    OUTPUT_PATH.chmod(0o600)
    receipt = {
        "status": "PASS",
        "gene": output["gene"],
        "variant_count": len(evidence),
        "phase_interpretation": output["phase_interpretation"],
        "raw_narrative_emitted": False,
        "genome_scale_values_emitted": False,
    }
    SAFE_RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    SAFE_RECEIPT_PATH.chmod(0o600)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
