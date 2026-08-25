import csv
import tempfile
import unittest
from pathlib import Path

from scripts.validate_track1_submission import EXPECTED_HEADERS, validate_track1_csv


def _row(**overrides):
    row = {
        "proband_id": "SYNTHETIC-ONLY",
        "chrom_1": "chr1",
        "pos_1": "100000",
        "ref_1": "A",
        "alt_1": "G",
        "chrom_2": "chr1",
        "pos_2": "100500",
        "ref_2": "C",
        "alt_2": "T",
        "epcr": "0.90",
        "finding_type": "primary",
        "notes": "Synthetic fixture; not patient-derived.",
    }
    row.update(overrides)
    return row


class Track1SubmissionValidatorTests(unittest.TestCase):
    def _validate(self, rows, headers=EXPECTED_HEADERS):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "submission.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
            return validate_track1_csv(path)

    def test_valid_pair_passes(self):
        result = self._validate([_row()])
        self.assertTrue(result.ok, result.errors)

    def test_partial_pair_fails(self):
        result = self._validate([_row(alt_2="")])
        self.assertFalse(result.ok)
        self.assertTrue(any("all four second-variant" in error for error in result.errors))

    def test_epcr_must_be_strictly_decreasing(self):
        result = self._validate([
            _row(epcr="0.80"),
            _row(chrom_1="chr2", pos_1="200000", chrom_2="", pos_2="", ref_2="", alt_2="", epcr="0.90"),
        ])
        self.assertFalse(result.ok)
        self.assertTrue(any("strictly decreasing" in error for error in result.errors))

    def test_reversed_duplicate_pair_fails(self):
        result = self._validate([
            _row(epcr="0.90"),
            _row(
                chrom_1="chr1",
                pos_1="100500",
                ref_1="C",
                alt_1="T",
                chrom_2="chr1",
                pos_2="100000",
                ref_2="A",
                alt_2="G",
                epcr="0.80",
            ),
        ])
        self.assertFalse(result.ok)
        self.assertTrue(any("duplicate candidate" in error for error in result.errors))

    def test_mixed_proband_ids_fail(self):
        result = self._validate([
            _row(epcr="0.90"),
            _row(proband_id="OTHER-SYNTHETIC", chrom_1="chr2", pos_1="200000", chrom_2="", pos_2="", ref_2="", alt_2="", epcr="0.80"),
        ])
        self.assertFalse(result.ok)
        self.assertIn("all rows must use the same proband_id", result.errors)

    def test_wrong_headers_fail(self):
        headers = EXPECTED_HEADERS[:-1]
        row = {key: value for key, value in _row().items() if key in headers}
        result = self._validate([row], headers=headers)
        self.assertFalse(result.ok)
        self.assertTrue(any("headers must exactly match" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
