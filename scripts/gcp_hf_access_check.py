#!/usr/bin/env python3
"""Emit only safe Hugging Face authentication and repository status codes."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from huggingface_hub import HfApi, get_token, hf_hub_url

from gcp_private_intake import REPO_ID, classify


def status(url: str, token: str) -> int:
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return int(response.status)
    except urllib.error.HTTPError as error:
        return int(error.code)


def head_status(url: str, token: str) -> int:
    request = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {token}"}, method="HEAD"
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return int(response.status)
    except urllib.error.HTTPError as error:
        return int(error.code)


def main() -> int:
    token = get_token()
    if not token:
        print(json.dumps({"token_present": False, "whoami_http": 0, "dataset_http": 0}))
        return 2
    whoami_http = status("https://huggingface.co/api/whoami-v2", token)
    dataset_http = status(f"https://huggingface.co/api/datasets/{REPO_ID}", token)
    api = HfApi()
    account_matches = api.whoami(token=token).get("name") == "svillalobos-gonzalez"
    entries = list(api.list_repo_tree(REPO_ID, repo_type="dataset", recursive=True, expand=True))
    paths = [entry.path for entry in entries if getattr(entry, "path", None) and hasattr(entry, "size")]
    variants, indexes, phenotypes = classify(paths)
    role_paths = {
        "variant": variants[0] if len(variants) == 1 else None,
        "index": indexes[0] if len(indexes) == 1 else None,
        "phenotype": phenotypes[0] if len(phenotypes) == 1 else None,
    }
    file_head_status = {
        role: head_status(hf_hub_url(REPO_ID, path, repo_type="dataset"), token)
        for role, path in role_paths.items()
        if path is not None
    }
    receipt = {
        "token_present": True,
        "account_matches": account_matches,
        "whoami_http": whoami_http,
        "dataset_http": dataset_http,
        "variant_candidate_count": len(variants),
        "index_candidate_count": len(indexes),
        "phenotype_candidate_count": len(phenotypes),
        "file_head_status": file_head_status,
    }
    print(json.dumps(receipt, sort_keys=True))
    return 0 if whoami_http == 200 and dataset_http == 200 and account_matches else 3


if __name__ == "__main__":
    raise SystemExit(main())
