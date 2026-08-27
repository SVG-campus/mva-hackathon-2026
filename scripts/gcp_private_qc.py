#!/usr/bin/env python3
"""Run fail-closed private VCF/phenotype QC and emit only aggregate status."""

from __future__ import annotations

import json
import os
import re
import subprocess
import zipfile
from pathlib import Path
from xml.etree import ElementTree


BASE_DIR = Path("/srv/mva-private")
MANIFEST_PATH = BASE_DIR / "private_manifest.json"
DETAIL_PATH = BASE_DIR / "private_qc_detail.json"
SAFE_RECEIPT_PATH = BASE_DIR / "qc_safe_receipt.json"
PHENOPACKET_PATH = BASE_DIR / "phenopacket.yml"
CLINICAL_TEXT_PATH = BASE_DIR / "clinical_text.txt"
HPO_RE = re.compile(r"HP:\d{7}")
HPO_OBO_PATH = Path("/opt/mva-public/hp.obo")
HPO_MAPPING_PATH = BASE_DIR / "hpo_mapping_private.json"
NEGATION_RE = re.compile(
    r"\b(?:no|not|without|denies|denied|negative\s+for|absence\s+of)\b",
    flags=re.IGNORECASE,
)


def run(args: list[str], *, text: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=False, capture_output=True, text=text)


def has_at_least_one_record(vcf: Path) -> bool:
    process = subprocess.Popen(
        ["bcftools", "view", "--no-header", str(vcf)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdout is not None
    first_record = process.stdout.readline()
    process.terminate()
    try:
        process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
    return bool(first_record.strip())


def extract_clinical_text(path: Path) -> str:
    lower = path.name.lower()
    if lower.endswith(".docx"):
        chunks: list[str] = []
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                if not name.startswith("word/") or not name.endswith(".xml"):
                    continue
                root = ElementTree.fromstring(archive.read(name))
                chunks.extend(node.text for node in root.iter() if node.text)
        return "\n".join(chunks)
    if lower.endswith((".txt", ".json", ".yaml", ".yml")):
        return path.read_text(encoding="utf-8", errors="replace")
    raise RuntimeError("Fail closed: unsupported clinical document format")


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _normalise_phrase(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def _load_hpo_phrases(path: Path) -> dict[str, tuple[str, str]]:
    if not path.is_file():
        raise RuntimeError("Fail closed: local HPO ontology is unavailable")
    phrase_candidates: dict[str, set[tuple[str, str]]] = {}
    current: dict[str, object] | None = None

    def flush() -> None:
        nonlocal current
        if not current or current.get("obsolete") or not current.get("id") or not current.get("name"):
            current = None
            return
        hpo_id = str(current["id"])
        label = str(current["name"])
        for term in [label, *list(current.get("synonyms", []))]:
            phrase = _normalise_phrase(str(term))
            tokens = phrase.split()
            if not phrase or (len(tokens) == 1 and len(phrase) < 8):
                continue
            phrase_candidates.setdefault(phrase, set()).add((hpo_id, label))
        current = None

    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if line.startswith("[") and line.endswith("]"):
            flush()
            current = {"synonyms": []} if line == "[Term]" else None
        elif current is None:
            continue
        elif line.startswith("id: HP:"):
            current["id"] = line.removeprefix("id: ")
        elif line.startswith("name: "):
            current["name"] = line.removeprefix("name: ")
        elif line.startswith("synonym: "):
            match = re.match(r'synonym: "([^"]+)"', line)
            if match:
                current["synonyms"].append(match.group(1))  # type: ignore[union-attr]
        elif line == "is_obsolete: true":
            current["obsolete"] = True
    flush()
    return {
        phrase: next(iter(values))
        for phrase, values in phrase_candidates.items()
        if len(values) == 1
    }


def map_hpo_terms(clinical_text: str, ontology_path: Path = HPO_OBO_PATH) -> list[dict[str, str]]:
    """Map only unambiguous exact HPO names/synonyms outside negated clauses."""
    phrases = _load_hpo_phrases(ontology_path)
    matches: dict[str, dict[str, str]] = {}
    for segment in re.split(r"[\r\n.!?;]+", clinical_text):
        normalised = _normalise_phrase(segment)
        if not normalised:
            continue
        tokens = normalised.split()
        for size in range(1, min(12, len(tokens)) + 1):
            for start in range(0, len(tokens) - size + 1):
                phrase = " ".join(tokens[start : start + size])
                if phrase not in phrases:
                    continue
                prefix = " ".join(tokens[max(0, start - 8) : start])
                if NEGATION_RE.search(prefix):
                    continue
                hpo_id, label = phrases[phrase]
                matches[hpo_id] = {
                    "id": hpo_id,
                    "label": label,
                    "matched_term": phrase,
                    "method": "exact_hpo_name_or_synonym",
                }
    return [matches[hpo_id] for hpo_id in sorted(matches)]


def main() -> int:
    os.umask(0o077)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    vcf = Path(manifest["local_files"]["variant"])
    index = Path(manifest["local_files"]["index"])
    phenotype = Path(manifest["local_files"]["phenotype"])
    if not all(path.is_file() for path in (vcf, index, phenotype)):
        raise RuntimeError("Fail closed: a selected private input is missing")
    for role, path in (("variant", vcf), ("index", index), ("phenotype", phenotype)):
        if path.stat().st_size != int(manifest["sizes"][role]):
            raise RuntimeError(f"Fail closed: {role} file size differs from repository metadata")

    header_result = run(["bcftools", "view", "--header-only", str(vcf)])
    if header_result.returncode != 0 or not header_result.stdout.startswith("##fileformat=VCF"):
        raise RuntimeError("Fail closed: VCF header validation failed")
    header = header_result.stdout

    sample_result = run(["bcftools", "query", "--list-samples", str(vcf)])
    samples = [line.strip() for line in sample_result.stdout.splitlines() if line.strip()]
    if sample_result.returncode != 0 or len(samples) != 1:
        raise RuntimeError("Fail closed: expected exactly one VCF sample")
    sample_id = samples[0]

    count_result = run(["bcftools", "index", "--nrecords", str(vcf)])
    if count_result.returncode != 0:
        raise RuntimeError("Fail closed: indexed record count failed")
    record_count = int(count_result.stdout.strip())
    record_count_source = "index"
    if record_count <= 0:
        if not has_at_least_one_record(vcf):
            raise RuntimeError("Fail closed: VCF contains no readable records")
        record_count = 1
        record_count_source = "stream_presence_lower_bound"

    build_is_grch38 = (
        "GRCh38" in header
        or "hg38" in header.lower()
        or bool(re.search(r"##contig=<ID=(?:chr)?1,length=248956422(?:,|>)", header))
    )
    if not build_is_grch38:
        raise RuntimeError("Fail closed: GRCh38 could not be established")
    format_fields = {
        match.group(1)
        for match in re.finditer(r"^##FORMAT=<ID=([^,>]+)", header, flags=re.MULTILINE)
    }
    if "GT" not in format_fields:
        raise RuntimeError("Fail closed: genotype field is absent")

    clinical_text = extract_clinical_text(phenotype)
    CLINICAL_TEXT_PATH.write_text(clinical_text, encoding="utf-8")
    CLINICAL_TEXT_PATH.chmod(0o600)
    hpo_ids = sorted(set(HPO_RE.findall(clinical_text)))
    hpo_source = "explicit_identifiers"
    if not hpo_ids:
        mapped_terms = map_hpo_terms(clinical_text)
        hpo_ids = [item["id"] for item in mapped_terms]
        hpo_source = "exact_ontology_phrase"
        HPO_MAPPING_PATH.write_text(json.dumps(mapped_terms, indent=2) + "\n", encoding="utf-8")
        HPO_MAPPING_PATH.chmod(0o600)
    if not hpo_ids:
        raise RuntimeError("Fail closed: no explicit or unambiguous exact HPO terms found")

    phenopacket_lines = [
        "---",
        f"id: {yaml_quote(sample_id)}",
        "subject:",
        f"  id: {yaml_quote(sample_id)}",
        "phenotypicFeatures:",
    ]
    for hpo_id in hpo_ids:
        phenopacket_lines.extend(["  - type:", f"      id: {hpo_id}"])
    phenopacket_lines.extend(
        [
            "htsFiles:",
            f"  - uri: {yaml_quote(str(vcf))}",
            "    htsFormat: VCF",
            "    genomeAssembly: hg38",
            "metaData:",
            "  created: '2026-08-27T00:00:00Z'",
            "  createdBy: private-frozen-pipeline",
            "  resources: []",
            "  phenopacketSchemaVersion: 1.0",
        ]
    )
    PHENOPACKET_PATH.write_text("\n".join(phenopacket_lines) + "\n", encoding="utf-8")
    PHENOPACKET_PATH.chmod(0o600)

    detail = {
        "sample_id": sample_id,
        "record_count": record_count,
        "record_count_source": record_count_source,
        "build": "GRCh38",
        "format_fields": sorted(format_fields),
        "hpo_ids": hpo_ids,
        "hpo_source": hpo_source,
        "vcf": str(vcf),
        "index": str(index),
        "phenotype": str(phenotype),
        "phenopacket": str(PHENOPACKET_PATH),
    }
    DETAIL_PATH.write_text(json.dumps(detail, indent=2) + "\n", encoding="utf-8")
    DETAIL_PATH.chmod(0o600)

    receipt = {
        "status": "PASS",
        "sample_count": 1,
        "record_count_positive": True,
        "record_count_source": record_count_source,
        "build": "GRCh38",
        "has_gt": True,
        "has_dp": "DP" in format_fields,
        "has_gq": "GQ" in format_fields,
        "hpo_id_count": len(hpo_ids),
        "hpo_source": hpo_source,
        "phenopacket_created": True,
    }
    SAFE_RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    SAFE_RECEIPT_PATH.chmod(0o600)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
