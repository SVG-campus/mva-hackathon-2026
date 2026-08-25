# Data governance gates

## Current status

`HOLD_REAL_DATA`: the official dataset is gated and contains a real child's genomic and clinical data. The organizers' public discussion about third-party LLM/API handling is unresolved as of 2026-08-25, and the local workstation has insufficient free space for the published storage requirement.

## Hard gates before real-data execution

1. **Organizer clarification** — written answer covering hosted AI/API use, zero-retention requirements, derived-data scope, and deletion of provider logs.
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
