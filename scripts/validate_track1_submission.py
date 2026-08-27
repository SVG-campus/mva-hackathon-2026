"""Fail-closed validation for a Track 1 submission CSV.

This checks public schema and ranking mechanics only. It does not inspect,
interpret, or validate the scientific truth of any candidate.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from dataclasses import dataclass, field
from pathlib import Path


EXPECTED_HEADERS = [
    "proband_id",
    "chrom_1",
    "pos_1",
    "ref_1",
    "alt_1",
    "chrom_2",
    "pos_2",
    "ref_2",
    "alt_2",
    "epcr",
    "finding_type",
    "notes",
]

OFFICIAL_PROBAND_ID = "PROBAND01"

STANDARD_CHROMOSOME = re.compile(r"^chr(?:[1-9]|1[0-9]|2[0-2]|X|Y|M|MT)$")
SECOND_VARIANT_FIELDS = ("chrom_2", "pos_2", "ref_2", "alt_2")


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    row_count: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def _positive_integer(value: str) -> bool:
    try:
        return int(value) > 0 and str(int(value)) == value
    except ValueError:
        return False


def _variant_key(row: dict[str, str], suffix: str) -> tuple[str, int, str, str]:
    return (
        row[f"chrom_{suffix}"],
        int(row[f"pos_{suffix}"]),
        row[f"ref_{suffix}"].upper(),
        row[f"alt_{suffix}"].upper(),
    )


def validate_track1_csv(path: str | Path) -> ValidationResult:
    result = ValidationResult()
    csv_path = Path(path)

    try:
        handle = csv_path.open("r", encoding="utf-8-sig", newline="")
    except OSError as exc:
        result.errors.append(f"cannot open CSV: {exc}")
        return result

    with handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXPECTED_HEADERS:
            result.errors.append(
                "headers must exactly match the official template in this order: "
                + ",".join(EXPECTED_HEADERS)
            )
            return result
        rows = []
        for raw_row in reader:
            if None in raw_row:
                result.errors.append("a row contains more fields than the header")
                continue
            rows.append({key: (value or "").strip() for key, value in raw_row.items()})

    result.row_count = len(rows)
    if not 1 <= result.row_count <= 10:
        result.errors.append("submission must contain between 1 and 10 candidate rows")

    proband_ids: set[str] = set()
    candidate_keys: set[tuple[tuple[str, int, str, str], ...]] = set()
    previous_epcr = math.inf

    for index, row in enumerate(rows, start=2):
        label = f"CSV row {index}"
        if not row["proband_id"]:
            result.errors.append(f"{label}: proband_id is required")
        else:
            proband_ids.add(row["proband_id"])
            if row["proband_id"] != OFFICIAL_PROBAND_ID:
                result.errors.append(
                    f"{label}: proband_id must be the official challenge identifier {OFFICIAL_PROBAND_ID}"
                )

        for suffix in ("1",):
            for field_name in (f"chrom_{suffix}", f"pos_{suffix}", f"ref_{suffix}", f"alt_{suffix}"):
                if not row[field_name]:
                    result.errors.append(f"{label}: {field_name} is required")

        second_present = [bool(row[name]) for name in SECOND_VARIANT_FIELDS]
        if any(second_present) and not all(second_present):
            result.errors.append(
                f"{label}: a compound-heterozygous candidate must populate all four second-variant fields"
            )

        for suffix in ("1", "2"):
            chrom = row[f"chrom_{suffix}"]
            pos = row[f"pos_{suffix}"]
            ref = row[f"ref_{suffix}"]
            alt = row[f"alt_{suffix}"]
            if not any((chrom, pos, ref, alt)):
                continue
            if chrom and not STANDARD_CHROMOSOME.fullmatch(chrom):
                result.errors.append(
                    f"{label}: chrom_{suffix} must use a standard GRCh38-style chr prefix"
                )
            if pos and not _positive_integer(pos):
                result.errors.append(f"{label}: pos_{suffix} must be a positive integer")
            if ref and alt and ref.upper() == alt.upper():
                result.errors.append(f"{label}: ref_{suffix} and alt_{suffix} cannot be identical")

        try:
            epcr = float(row["epcr"])
        except ValueError:
            result.errors.append(f"{label}: epcr must be numeric")
            epcr = math.nan
        if not math.isfinite(epcr) or not 0 < epcr <= 1:
            result.errors.append(f"{label}: epcr must be finite and in (0, 1]")
        elif epcr >= previous_epcr:
            result.errors.append(
                f"{label}: epcr values must be strictly decreasing to make rank deterministic"
            )
        previous_epcr = epcr

        if row["finding_type"] not in {"primary", "secondary"}:
            result.errors.append(f"{label}: finding_type must be primary or secondary")

        if all((row["chrom_1"], row["pos_1"], row["ref_1"], row["alt_1"])) and _positive_integer(row["pos_1"]):
            variants = [_variant_key(row, "1")]
            if all(second_present) and _positive_integer(row["pos_2"]):
                variants.append(_variant_key(row, "2"))
            candidate_key = tuple(sorted(variants))
            if candidate_key in candidate_keys:
                result.errors.append(f"{label}: duplicate candidate row, including reversed pairs")
            candidate_keys.add(candidate_key)

        if row["finding_type"] == "secondary":
            result.warnings.append(
                f"{label}: the pinned public evaluator still ranks secondary rows; replay locally before submission"
            )

    if len(proband_ids) > 1:
        result.errors.append("all rows must use the same proband_id")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    result = validate_track1_csv(args.csv_path)

    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")
    if result.ok:
        print(f"PASS: {result.row_count} Track 1 candidate row(s) passed structural validation")
        return 0
    print(f"FAIL: {len(result.errors)} structural error(s)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
