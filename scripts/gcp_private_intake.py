#!/usr/bin/env python3
"""Download only the gated VCF, index, and phenotype file without logging names."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


REPO_ID = "SageBio/mva-hackathon-2026-data"
BASE_DIR = Path("/srv/mva-private")
INPUT_DIR = BASE_DIR / "input"
MANIFEST_PATH = BASE_DIR / "private_manifest.json"
SAFE_RECEIPT_PATH = BASE_DIR / "intake_safe_receipt.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def classify(paths: list[str]) -> tuple[list[str], list[str], list[str]]:
    variants: list[str] = []
    indexes: list[str] = []
    phenotypes: list[str] = []
    for repo_path in paths:
        lower = repo_path.lower()
        if lower.endswith((".vcf.gz", ".vcf.bgz", ".bcf", ".vcf")):
            variants.append(repo_path)
        elif lower.endswith((".tbi", ".csi")):
            indexes.append(repo_path)
        elif (
            ("phenotype" in lower or "clinical" in lower)
            and lower.endswith((".docx", ".json", ".yaml", ".yml", ".txt", ".pdf"))
        ):
            phenotypes.append(repo_path)
    return variants, indexes, phenotypes


def main() -> int:
    from huggingface_hub import HfApi, hf_hub_download

    os.umask(0o077)
    INPUT_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)

    api = HfApi()
    info = api.dataset_info(REPO_ID)
    entries = list(api.list_repo_tree(REPO_ID, repo_type="dataset", recursive=True, expand=True))
    files = [entry for entry in entries if getattr(entry, "path", None) and hasattr(entry, "size")]
    paths = [entry.path for entry in files]
    sizes = {entry.path: int(entry.size or 0) for entry in files}
    variants, indexes, phenotypes = classify(paths)

    if len(variants) != 1:
        raise RuntimeError("Fail closed: expected exactly one primary variant file")
    variant = variants[0]
    matching_indexes = [
        item
        for item in indexes
        if item in {variant + ".tbi", variant + ".csi"}
        or (variant.endswith(".gz") and item in {variant[:-3] + ".tbi", variant[:-3] + ".csi"})
    ]
    if len(matching_indexes) != 1:
        raise RuntimeError("Fail closed: expected exactly one matching variant index")
    if len(phenotypes) != 1:
        raise RuntimeError("Fail closed: expected exactly one clinical phenotype file")

    selected = {
        "variant": variant,
        "index": matching_indexes[0],
        "phenotype": phenotypes[0],
    }
    local_files: dict[str, str] = {}
    hashes: dict[str, str] = {}
    for role, repo_path in selected.items():
        local_path = Path(
            hf_hub_download(
                repo_id=REPO_ID,
                repo_type="dataset",
                filename=repo_path,
                revision=info.sha,
                local_dir=INPUT_DIR,
            )
        )
        local_files[role] = str(local_path)
        hashes[role] = sha256_file(local_path)

    manifest = {
        "repo_id": REPO_ID,
        "repo_sha": info.sha,
        "selected_repo_paths": selected,
        "local_files": local_files,
        "sizes": {role: sizes[path] for role, path in selected.items()},
        "sha256": hashes,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    MANIFEST_PATH.chmod(0o600)

    receipt = {
        "status": "PASS",
        "repo_sha_recorded": bool(info.sha),
        "variant_file_count": 1,
        "index_file_count": 1,
        "phenotype_file_count": 1,
        "downloaded_bytes": sum(manifest["sizes"].values()),
        "hash_count": len(hashes),
    }
    SAFE_RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    SAFE_RECEIPT_PATH.chmod(0o600)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
