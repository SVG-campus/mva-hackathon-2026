from __future__ import annotations

import csv
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "challenge_reference"

EXPECTED_SHA256 = {
    "evaluation.py": "6d18b581e65a45e1ccc120071d588e740c2e42e983ff50704c60a40232b19180",
    "track1_submission_template.csv": "7b3ed41c091d34fb6c5622d049c7a3f46124211fc7ec02947e69daef8752755a",
    "methods_description_form.xlsx": "e160c3b12dff23584660de42fb13095ac1d592c991fff92714e6f7f6678249b4",
}

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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class ReferenceIntegrityTests(unittest.TestCase):
    def test_official_reference_hashes_are_frozen(self) -> None:
        for name, expected in EXPECTED_SHA256.items():
            with self.subTest(name=name):
                self.assertEqual(sha256(REFERENCE / name), expected)

    def test_track1_template_headers_are_exact(self) -> None:
        with (REFERENCE / "track1_submission_template.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            reader = csv.reader(handle)
            self.assertEqual(next(reader), EXPECTED_HEADERS)

    def test_track1_template_stays_within_row_limit(self) -> None:
        with (REFERENCE / "track1_submission_template.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertLessEqual(len(rows), 10)


if __name__ == "__main__":
    unittest.main()
