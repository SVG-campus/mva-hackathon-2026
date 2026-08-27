from pathlib import Path

from scripts.gcp_private_build_shortlist import _strict_epcr, read_pairs
from scripts.gcp_private_intake import classify
from scripts.gcp_private_qc import map_hpo_terms
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


def test_shortlist_parser_keeps_exact_ar_pairs(tmp_path: Path) -> None:
    output = tmp_path / "case.variants.tsv"
    header = [
        "#RANK",
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
    ]
    rows = [
        ["1", "BUB1B", "AR", "0.91", "0.80", "0.95", "1", "15", "100", "A", "G"],
        ["1", "BUB1B", "AR", "0.91", "0.80", "0.95", "1", "15", "200", "C", "T"],
        ["2", "OTHER", "AD", "0.80", "0.70", "0.90", "1", "1", "300", "G", "A"],
    ]
    output.write_text(
        "\n".join("\t".join(row) for row in [header, *rows]) + "\n",
        encoding="utf-8",
    )
    pairs = read_pairs(output)
    assert len(pairs) == 1
    assert pairs[0].gene == "BUB1B"
    assert [variant.pos for variant in pairs[0].variants] == [100, 200]


def test_shortlist_epcr_is_strictly_descending() -> None:
    values = _strict_epcr([0.7, 0.7, 0.9, 0.01])
    assert all(left > right for left, right in zip(values, values[1:]))
    assert all(0 < value <= 1 for value in values)


def test_hpo_fallback_maps_exact_terms_and_rejects_negation(tmp_path: Path) -> None:
    ontology = tmp_path / "hp.obo"
    ontology.write_text(
        """format-version: 1.2

[Term]
id: HP:0000252
name: Microcephaly
synonym: "Small head" EXACT []

[Term]
id: HP:0001250
name: Seizure
synonym: "Seizures" EXACT []
""",
        encoding="utf-8",
    )
    matches = map_hpo_terms("Microcephaly. No seizures.", ontology)
    assert [match["id"] for match in matches] == ["HP:0000252"]
