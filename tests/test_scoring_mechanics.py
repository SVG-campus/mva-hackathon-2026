from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from challenge_reference.evaluation import load_submission, score_proband


PROBAND = "PROBAND01"
TRUE_PAIR = frozenset(
    {
        ("chr2", 12_345_678, "T", "G"),
        ("chr15", 12_345_678, "T", "G"),
    }
)
FIELDS = [
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


def pair_row(epcr: float, finding_type: str = "primary") -> dict[str, object]:
    return {
        "proband_id": PROBAND,
        "chrom_1": "chr2",
        "pos_1": 12_345_678,
        "ref_1": "T",
        "alt_1": "G",
        "chrom_2": "chr15",
        "pos_2": 12_345_678,
        "ref_2": "T",
        "alt_2": "G",
        "epcr": epcr,
        "finding_type": finding_type,
        "notes": "synthetic fixture",
    }


def single_row(
    chrom: str,
    pos: int,
    ref: str,
    alt: str,
    epcr: float,
    finding_type: str = "primary",
) -> dict[str, object]:
    return {
        "proband_id": PROBAND,
        "chrom_1": chrom,
        "pos_1": pos,
        "ref_1": ref,
        "alt_1": alt,
        "chrom_2": "",
        "pos_2": "",
        "ref_2": "",
        "alt_2": "",
        "epcr": epcr,
        "finding_type": finding_type,
        "notes": "synthetic fixture",
    }


def evaluate(rows: list[dict[str, object]]):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "submission.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        loaded = load_submission(str(path))[PROBAND]
    return score_proband(PROBAND, loaded, TRUE_PAIR)


class ScoringMechanicsTests(unittest.TestCase):
    def test_exact_pair_at_rank_one_gets_full_score(self) -> None:
        result = evaluate(
            [
                pair_row(0.90),
                single_row("chr7", 300_000, "C", "T", 0.10, "secondary"),
            ]
        )
        self.assertEqual(result.full_match_rank, 1)
        self.assertEqual(result.rank_points, 100.0)
        self.assertEqual(result.f_max, 1.0)

    def test_split_pair_gets_partial_rank_credit_even_when_fmax_is_perfect(self) -> None:
        result = evaluate(
            [
                single_row("chr2", 12_345_678, "T", "G", 0.90),
                single_row("chr15", 12_345_678, "T", "G", 0.80),
            ]
        )
        self.assertIsNone(result.full_match_rank)
        self.assertEqual(result.partial_match_rank, 1)
        self.assertEqual(result.rank_points, 50.0)
        self.assertEqual(result.f_max, 1.0)

    def test_high_confidence_secondary_false_positive_is_not_ignored(self) -> None:
        result = evaluate(
            [
                single_row("chr7", 300_000, "C", "T", 0.90, "secondary"),
                pair_row(0.50),
            ]
        )
        self.assertEqual(result.full_match_rank, 2)
        self.assertEqual(result.rank_points, 50.0)
        self.assertAlmostEqual(result.f_max, 0.8)

    def test_true_pair_at_rank_six_gets_ten_points(self) -> None:
        false_rows = [
            single_row(f"chr{i}", 1_000 + i, "A", "C", 0.99 - i / 100)
            for i in range(1, 6)
        ]
        result = evaluate(false_rows + [pair_row(0.50)])
        self.assertEqual(result.full_match_rank, 6)
        self.assertEqual(result.rank_points, 10.0)

    def test_more_than_ten_rows_fails_closed(self) -> None:
        rows = [
            single_row("chr1", 1_000 + i, "A", "C", 0.99 - i / 100)
            for i in range(11)
        ]
        with self.assertRaisesRegex(ValueError, "max is 10"):
            evaluate(rows)

    def test_epcr_outside_open_closed_unit_interval_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "out of range"):
            evaluate([pair_row(0.0)])


if __name__ == "__main__":
    unittest.main()
