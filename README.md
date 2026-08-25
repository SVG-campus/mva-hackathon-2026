# MVA Hackathon 2026 — privacy-safe working repository

This repository is the local, reproducible preparation area for the SageBio **Rare Disease, Real Kid: MVA Hackathon 2026**.

Current status: **preliminary public-source, synthetic-scorer, and public-toolchain pass only**. No real-child genomic or clinical data have been downloaded into this repository, no live challenge submission has been made, and no medical or causal claim has been established.

## Selected development route

1. Build a public, reproducible Track 1 baseline that ranks exact compound-heterozygous pairs using call quality, rarity, inheritance, functional evidence, and phenotype similarity.
2. Compare it with a challenger that adds non-coding/splice analysis, the seven numbered MVA forms, and three lower-maturity no-miss genes.
3. Use Track 2 only after the causal pair and loss/gain-of-function mechanism pass a separate evidence gate.

The project is intentionally designed so public code operates on synthetic fixtures. Real-data execution must occur in an approved local-only environment and emit only a manually reviewed, non-identifying submission artifact.

## Reproduce the current preliminary checks

```powershell
& 'C:\Users\svillalobosgonzalez1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests -v
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
