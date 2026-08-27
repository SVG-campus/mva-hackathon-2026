#!/usr/bin/env python3
"""Build a bounded compound-heterozygous shortlist from private Exomiser TSVs.

The script stays on the isolated VM. It reads genome-scale outputs but writes at
most ten paired findings, plus a value-free execution receipt. EPCR values are
conservative ranking proxies, not clinically calibrated probabilities.
"""

from __future__ import annotations

import csv
import json
import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PRIVATE_DIR = Path("/srv/mva-private")
RUN_DIR = PRIVATE_DIR / "exomiser-runs"
QC_DETAIL = PRIVATE_DIR / "private_qc_detail.json"
SHORTLIST_PATH = PRIVATE_DIR / "candidate_shortlist_private.json"
CSV_PATH = PRIVATE_DIR / "track1_predictions_private.csv"
SAFE_RECEIPT_PATH = PRIVATE_DIR / "shortlist_safe_receipt.json"

CORE_MVA_GENES = frozenset({"BUB1B", "CEP57", "TRIP13", "CENATAC", "SMC5", "SLF2", "MAD1L1"})
NO_MISS_GENES = frozenset({"BUB1", "MAD2L1BP", "CEP192"})

CSV_FIELDS = [
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


@dataclass(frozen=True, order=True)
class Variant:
    chrom: str
    pos: int
    ref: str
    alt: str


@dataclass(frozen=True)
class PairResult:
    gene: str
    variants: tuple[Variant, Variant]
    rank: int
    combined_score: float
    phenotype_score: float
    variant_score: float
    max_frequency: float

    @property
    def key(self) -> tuple[str, tuple[Variant, Variant]]:
        return self.gene, self.variants


def _float(row: dict[str, str], name: str) -> float:
    value = (row.get(name) or "").strip()
    return float(value) if value else 0.0


def _variant(row: dict[str, str]) -> Variant:
    return Variant(
        chrom=(row.get("CONTIG") or "").strip().removeprefix("chr"),
        pos=int((row.get("START") or "0").strip()),
        ref=(row.get("REF") or "").strip().upper(),
        alt=(row.get("ALT") or "").strip().upper(),
    )


def read_pairs(path: Path) -> list[PairResult]:
    """Return exactly-two-variant AR gene scores from an Exomiser variants TSV."""
    groups: dict[tuple[int, str], list[dict[str, str]]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames:
            reader.fieldnames = [name.lstrip("#") for name in reader.fieldnames]
        required = {
            "RANK",
            "GENE_SYMBOL",
            "MOI",
            "EXOMISER_GENE_COMBINED_SCORE",
            "EXOMISER_GENE_PHENO_SCORE",
            "EXOMISER_GENE_VARIANT_SCORE",
            "CONTRIBUTING_VARIANT",
            "CONTIG",
            "START",
            "REF",
            "ALT",
        }
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise RuntimeError(f"Fail closed: unexpected Exomiser TSV schema in {path.name}")
        for row in reader:
            if (row.get("MOI") or "").strip().upper() != "AR":
                continue
            if (row.get("CONTRIBUTING_VARIANT") or "").strip() != "1":
                continue
            rank = int((row.get("RANK") or "0").strip())
            gene = (row.get("GENE_SYMBOL") or "").strip().upper()
            if rank <= 0 or not gene:
                continue
            groups[(rank, gene)].append(row)

    results: list[PairResult] = []
    for (rank, gene), rows in groups.items():
        variants = tuple(sorted({_variant(row) for row in rows}))
        if len(variants) != 2:
            continue
        first = rows[0]
        results.append(
            PairResult(
                gene=gene,
                variants=(variants[0], variants[1]),
                rank=rank,
                combined_score=_float(first, "EXOMISER_GENE_COMBINED_SCORE"),
                phenotype_score=_float(first, "EXOMISER_GENE_PHENO_SCORE"),
                variant_score=_float(first, "EXOMISER_GENE_VARIANT_SCORE"),
                max_frequency=max(_float(row, "MAX_FREQ") for row in rows),
            )
        )
    return sorted(results, key=lambda item: (item.rank, item.gene, item.variants))


def _one_tsv(case: str) -> Path:
    matches = sorted((RUN_DIR / case).glob("*.variants.tsv"))
    if len(matches) != 1:
        raise RuntimeError(f"Fail closed: expected one variants TSV for {case}, found {len(matches)}")
    return matches[0]


def _case_map(case: str) -> dict[tuple[str, tuple[Variant, Variant]], PairResult]:
    return {result.key: result for result in read_pairs(_one_tsv(case))}


def _panel_bonus(gene: str) -> tuple[float, str]:
    if gene in CORE_MVA_GENES:
        return 0.05, "core_mva"
    if gene in NO_MISS_GENES:
        return 0.02, "no_miss"
    return 0.0, "phenotype_wide"


def _rank_candidates(
    baseline: dict[tuple[str, tuple[Variant, Variant]], PairResult],
    challenger: dict[tuple[str, tuple[Variant, Variant]], PairResult],
    ablated: dict[tuple[str, tuple[Variant, Variant]], PairResult],
    shuffled: dict[tuple[str, tuple[Variant, Variant]], PairResult],
) -> list[dict[str, object]]:
    candidate_keys = set(baseline) | set(challenger)
    rarity_order = sorted(
        candidate_keys,
        key=lambda key: (
            (baseline.get(key) or challenger[key]).max_frequency,
            (baseline.get(key) or challenger[key]).rank,
            key,
        ),
    )
    rarity_ranks = {key: rank for rank, key in enumerate(rarity_order, start=1)}
    candidates: list[dict[str, object]] = []
    for key in candidate_keys:
        primary = baseline.get(key)
        secondary = challenger.get(key)
        anchor = primary or secondary
        assert anchor is not None
        ablated_result = ablated.get(key)
        shuffled_result = shuffled.get(key)
        baseline_score = primary.combined_score if primary else 0.0
        challenger_score = secondary.combined_score if secondary else 0.0
        control_score = max(
            ablated_result.combined_score if ablated_result else 0.0,
            shuffled_result.combined_score if shuffled_result else 0.0,
        )
        phenotype_delta = max(0.0, baseline_score - control_score)
        panel_bonus, panel_tier = _panel_bonus(anchor.gene)
        route_score = (
            (1.0 / primary.rank if primary else 0.0)
            + (0.5 / secondary.rank if secondary else 0.0)
            + 0.20 * phenotype_delta
            + panel_bonus
        )
        epcr_proxy = min(
            0.80,
            0.60 * max(baseline_score, challenger_score)
            + 0.10 * phenotype_delta
            + (0.05 if primary and secondary else 0.0)
            + panel_bonus,
        )
        candidates.append(
            {
                "gene": anchor.gene,
                "variants": [variant.__dict__ for variant in anchor.variants],
                "baseline_rank": primary.rank if primary else None,
                "challenger_rank": secondary.rank if secondary else None,
                "phenotype_ablation_rank": ablated_result.rank if ablated_result else None,
                "phenotype_shuffle_rank": shuffled_result.rank if shuffled_result else None,
                "rarity_only_rank": rarity_ranks[key],
                "pair_max_frequency_percent": anchor.max_frequency,
                "baseline_combined_score": baseline_score,
                "challenger_combined_score": challenger_score,
                "phenotype_specificity_delta": phenotype_delta,
                "panel_tier": panel_tier,
                "route_score": route_score,
                "epcr_proxy": epcr_proxy,
            }
        )
    candidates.sort(
        key=lambda item: (
            -float(item["route_score"]),
            int(item["baseline_rank"] or 10**9),
            str(item["gene"]),
        )
    )
    return candidates[:10]


def _strict_epcr(values: Iterable[float]) -> list[float]:
    output: list[float] = []
    previous = 0.81
    for value in values:
        calibrated = min(max(value, 0.01), previous - 0.001)
        calibrated = round(calibrated, 6)
        if calibrated <= 0:
            calibrated = round(max(0.001, previous / 2), 6)
        output.append(calibrated)
        previous = calibrated
    return output


def write_submission(proband_id: str, candidates: list[dict[str, object]]) -> None:
    epcr_values = _strict_epcr(float(candidate["epcr_proxy"]) for candidate in candidates)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for candidate, epcr in zip(candidates, epcr_values, strict=True):
            variants = candidate["variants"]
            assert isinstance(variants, list) and len(variants) == 2
            first, second = variants
            assert isinstance(first, dict) and isinstance(second, dict)
            writer.writerow(
                {
                    "proband_id": proband_id,
                    "chrom_1": first["chrom"],
                    "pos_1": first["pos"],
                    "ref_1": first["ref"],
                    "alt_1": first["alt"],
                    "chrom_2": second["chrom"],
                    "pos_2": second["pos"],
                    "ref_2": second["ref"],
                    "alt_2": second["alt"],
                    "epcr": epcr,
                    "finding_type": "primary",
                    "notes": (
                        f"{candidate['gene']} AR pair; {candidate['panel_tier']}; "
                        "Exomiser 15.1.0 rank proxy, not clinical probability"
                    ),
                }
            )
    CSV_PATH.chmod(0o600)


def main() -> int:
    os.umask(0o077)
    detail = json.loads(QC_DETAIL.read_text(encoding="utf-8"))
    candidates = _rank_candidates(
        _case_map("baseline_exome"),
        _case_map("challenger_introns"),
        _case_map("phenotype_ablation"),
        _case_map("phenotype_shuffle"),
    )
    if not candidates:
        raise RuntimeError("Fail closed: no two-variant AR candidates survived")
    SHORTLIST_PATH.write_text(json.dumps(candidates, indent=2) + "\n", encoding="utf-8")
    SHORTLIST_PATH.chmod(0o600)
    write_submission(str(detail["sample_id"]), candidates)
    receipt = {
        "status": "PASS",
        "candidate_count": len(candidates),
        "all_candidates_are_pairs": all(len(item["variants"]) == 2 for item in candidates),
        "epcr_strictly_descending": True,
        "genome_scale_values_emitted": False,
    }
    SAFE_RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    SAFE_RECEIPT_PATH.chmod(0o600)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
