# Data governance gates

## Current status

`HOLD_REAL_DATA`: the official dataset is gated and contains a real child's genomic and clinical data. On 2026-08-26, SageBio organization member Luca Foschini, identifying himself as Sage's President, replied in public discussion #2 that the team will provide point-by-point clarification and instructed participants to use a conservative interpretation of every data-use clause in the meantime. This is authoritative interim guidance to keep the hosted-AI/API gate closed, not permission to process patient-derived material through an agent or provider. The local workstation also has insufficient free space for the published storage requirement.

Interim-guidance source: https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/2 (comment timestamp `2026-08-26T04:54:39Z`).

## Hard gates before real-data execution

1. **Organizer clarification** — final point-by-point written answer covering hosted AI/API use, zero-retention requirements, derived-data scope, and deletion of provider logs. The 2026-08-26 interim answer explicitly requires conservative interpretation and does not satisfy this gate.
2. **Storage** — at least 150 GB of approved encrypted working space, with backups and sync disabled unless explicitly covered by the data agreement.
3. **Isolation** — a local-only compute path that does not send patient-level coordinates, alleles, HPO terms, logs, prompts, or derived rankings to hosted services.
4. **Provenance** — record source hashes, tool versions, reference genome build, annotation versions, commands, and timestamps without copying patient-level values into the public receipt.
5. **Publication review** — manually inspect every public artifact for identifiers and patient-derived values before commit or upload.
6. **Deletion** — delete source and derived data from every environment within 30 days after challenge close and complete the organizer-required confirmation manually.

## Falsifiers and stop rules

- Any uncertainty about whether a field is identifying or derived from the child stops export.
- Any network call from the real-data environment stops the run until reviewed.
- Any public artifact containing a real coordinate, allele, HPO term, filename, screenshot, or log fails closed.
- No medication candidate is represented as treatment advice or clinical evidence.
