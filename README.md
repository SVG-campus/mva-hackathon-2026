# MVA Hackathon 2026 — privacy-safe working repository

This repository is the local, reproducible preparation area for the SageBio **Rare Disease, Real Kid: MVA Hackathon 2026**.

Current status: **public-source, synthetic-scorer, public-toolchain, private-intake/QC, four-route analysis, bounded candidate review, and Model 1 packaging checks pass**. Gated inputs were processed only inside the approved ephemeral GCP boundary. No raw genomic file, clinical narrative, genome-scale table, or reconstructive intermediate entered this repository; only organizer-permitted short findings and aggregate receipts were reduced from the private run. No live challenge submission has been made, and no medical or causal claim has been established.

## Selected development route

1. Build a public, reproducible Track 1 baseline that ranks exact compound-heterozygous pairs using call quality, rarity, inheritance, functional evidence, and phenotype similarity.
2. Compare it with Exomiser's documented exome-with-introns challenger, retaining splice-relevant intronic variants while treating the seven numbered MVA forms and three lower-maturity no-miss genes as a soft feature rather than a hard exclusion.
3. Use Track 2 only after the causal pair and loss/gain-of-function mechanism pass a separate evidence gate.

The project is intentionally designed so public code operates on synthetic fixtures. Real-data execution occurs only in the approved isolated environment and emits at most a short, manually reviewed finding set and submission artifact permitted by the organizer's written guidance.

## Reproduce the current preliminary checks

```powershell
python -m pytest -q --basetemp=local_dev\pytest-readme
```

The current receipt is **20 tests passing**. To validate a structurally complete Track 1 CSV without submitting it:

```powershell
& 'C:\Users\svillalobosgonzalez1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts\validate_track1_submission.py submission\synthetic\svillalobos-gonzalez_synthetic-dry-run.csv
```

## Important files

- `AGENTS.md` — data, action, and evidence boundaries.
- `docs/SOURCE_MANIFEST.md` — frozen official source versions and hashes.
- `docs/DATA_GOVERNANCE.md` — privacy, retention, and publication gates.
- `docs/DECISION_PACKET.md` — frozen route decision, evidence ceiling, falsifiers, and budgets.
- `docs/GCP_RUNBOOK.md` — tested public-only ephemeral design and remaining private-data gates.
- `docs/ORGANIZER_QUESTIONS.md` — unresolved questions for the user to post or email manually.
- `docs/PUBLIC_PREFLIGHT_RECEIPT.md` — public GCP/Exomiser test, retained failures, and teardown proof.
- `docs/RESEARCH_GAP_MATRIX.md` — searched-versus-known coverage and decisive open gaps.
- `docs/SUBMISSION_WALKTHROUGH.md` — calendar and manual submission checkpoints.
- `docs/TOOLCHAIN.md` — pinned public analysis stack, versions, integrity limits, and licenses.
- `challenge_reference/evaluation.py` — unmodified public Track 1 evaluator snapshot.
- `tests/test_scoring_mechanics.py` — synthetic tests of evaluator behavior.
- `scripts/validate_track1_submission.py` — fail-closed official-schema and rank validation before evaluator replay.
- `submission/track1_report_scaffold.md` — public-safe report structure with no patient-specific result.
- `submission/public/` — publication-reviewed Model 1 CSV, report, evidence card, and methods workbook prepared for the final owner gate.
- `submission/synthetic/` — artificial dry-run files that must never be uploaded to the challenge.
