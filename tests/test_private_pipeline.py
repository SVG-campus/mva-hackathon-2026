from pathlib import Path

from scripts.gcp_private_intake import classify
from scripts.gcp_private_run_exomiser import write_packet


def test_private_intake_classifies_only_frozen_roles() -> None:
    variants, indexes, phenotypes = classify(
        [
            "README.md",
            "synthetic/sample.vcf.gz",
            "synthetic/sample.vcf.gz.tbi",
            "clinical/phenotype.docx",
            "reads/sample_R1.fastq.gz",
        ]
    )
    assert variants == ["synthetic/sample.vcf.gz"]
    assert indexes == ["synthetic/sample.vcf.gz.tbi"]
    assert phenotypes == ["clinical/phenotype.docx"]


def test_control_phenopacket_contains_no_patient_values(tmp_path: Path) -> None:
    output = tmp_path / "control.yml"
    write_packet(output, "SYNTHETIC", "/private/synthetic.vcf.gz", [])
    text = output.read_text(encoding="utf-8")
    assert "SYNTHETIC" in text
    assert "phenotypicFeatures: []" in text
    assert "genomeAssembly: hg38" in text
