#!/usr/bin/env python3
"""Run frozen Exomiser baseline, challenger, and negative controls privately."""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path


PRIVATE_DIR = Path("/srv/mva-private")
PUBLIC_DIR = Path("/opt/mva-public")
CLI_DIR = PUBLIC_DIR / "exomiser-cli-15.1.0"
JAR_PATH = CLI_DIR / "exomiser-cli-15.1.0.jar"
DATA_DIR = CLI_DIR / "data"
QC_DETAIL = PRIVATE_DIR / "private_qc_detail.json"
RUN_DIR = PRIVATE_DIR / "exomiser-runs"
PROPERTIES_PATH = PRIVATE_DIR / "application-hg38-2602.properties"
SAFE_RECEIPT_PATH = PRIVATE_DIR / "exomiser_safe_receipt.json"

SHUFFLED_HPO = ["HP:0000365", "HP:0001250", "HP:0002090"]


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def write_packet(path: Path, sample_id: str, vcf: str, hpo_ids: list[str]) -> None:
    lines = [
        "---",
        f"id: {yaml_quote(sample_id)}",
        "subject:",
        f"  id: {yaml_quote(sample_id)}",
    ]
    if hpo_ids:
        lines.append("phenotypicFeatures:")
        for hpo_id in hpo_ids:
            lines.extend(["  - type:", f"      id: {hpo_id}"])
    else:
        lines.append("phenotypicFeatures: []")
    lines.extend(
        [
            "htsFiles:",
            f"  - uri: {yaml_quote(vcf)}",
            "    htsFormat: VCF",
            "    genomeAssembly: hg38",
            "metaData:",
            "  created: '2026-08-27T00:00:00Z'",
            "  createdBy: private-frozen-pipeline",
            "  resources: []",
            "  phenopacketSchemaVersion: 1.0",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path.chmod(0o600)


def run_case(
    name: str,
    analysis_option: str,
    analysis_value: str,
    packet: Path,
    vcf: str,
) -> dict[str, object]:
    output_dir = RUN_DIR / name
    output_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    log_path = RUN_DIR / f"{name}.log"
    command = [
        "java",
        "-Xmx20g",
        f"-Dspring.config.location=file:{PROPERTIES_PATH}",
        "-jar",
        str(JAR_PATH),
        "analyse",
        analysis_option,
        analysis_value,
        "--sample",
        str(packet),
        "--vcf",
        vcf,
        "--assembly",
        "hg38",
        "--output-directory",
        str(output_dir),
        "--output-filename",
        name,
        "--output-format=JSON,TSV_GENE,TSV_VARIANT",
    ]
    started = time.monotonic()
    with log_path.open("w", encoding="utf-8") as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
    runtime_seconds = round(time.monotonic() - started, 3)
    if result.returncode != 0:
        raise RuntimeError(f"Fail closed: Exomiser case {name} failed")
    outputs = [path for path in output_dir.iterdir() if path.is_file()]
    if not outputs:
        raise RuntimeError(f"Fail closed: Exomiser case {name} produced no outputs")
    return {
        "status": "PASS",
        "runtime_seconds": runtime_seconds,
        "output_file_count": len(outputs),
        "output_extensions": sorted({path.suffix.lower() for path in outputs}),
    }


def main() -> int:
    os.umask(0o077)
    if not (PUBLIC_DIR / "exomiser_install.done").is_file():
        raise RuntimeError("Fail closed: public Exomiser installation is incomplete")
    if not JAR_PATH.is_file() or not QC_DETAIL.is_file():
        raise RuntimeError("Fail closed: Exomiser or private QC input is missing")

    detail = json.loads(QC_DETAIL.read_text(encoding="utf-8"))
    sample_id = detail["sample_id"]
    vcf = detail["vcf"]
    baseline_packet = Path(detail["phenopacket"])
    frequency_packet = PRIVATE_DIR / "phenopacket-frequency-only.yml"
    shuffled_packet = PRIVATE_DIR / "phenopacket-shuffled.yml"
    write_packet(frequency_packet, sample_id, vcf, [])
    write_packet(shuffled_packet, sample_id, vcf, SHUFFLED_HPO)

    PROPERTIES_PATH.write_text(
        "\n".join(
            [
                f"exomiser.data-directory={DATA_DIR}",
                "exomiser.hg38.data-version=2602",
                "exomiser.phenotype.data-version=2602",
                "",
            ]
        ),
        encoding="utf-8",
    )
    PROPERTIES_PATH.chmod(0o600)
    RUN_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)

    cases = {
        "baseline_exome": ("--preset", "exome", baseline_packet),
        "challenger_introns": (
            "--analysis",
            str(CLI_DIR / "examples" / "preset-exome-analysis-with-introns.yml"),
            baseline_packet,
        ),
        "phenotype_ablation": ("--preset", "exome", frequency_packet),
        "phenotype_shuffle": ("--preset", "exome", shuffled_packet),
    }
    receipt: dict[str, object] = {"status": "PASS", "case_count": len(cases), "cases": {}}
    for name, (analysis_option, analysis_value, packet) in cases.items():
        receipt["cases"][name] = run_case(  # type: ignore[index]
            name,
            analysis_option,
            analysis_value,
            packet,
            vcf,
        )

    SAFE_RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    SAFE_RECEIPT_PATH.chmod(0o600)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
