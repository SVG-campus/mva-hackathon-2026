# Data governance gates

## Current status

`PRIVATE_RUN_REDUCED_PENDING_TEARDOWN`: the official dataset is gated and contains a real child's genomic and clinical data. On 2026-08-26, Sage's Chief Privacy and Compliance Officer supplied point-by-point guidance in public discussion #2. Hosted software may process the data only as a tool: it must take no rights in inputs or outputs, perform no training on them, and retain content only for a limited operational purpose. Zero retention and local inference are not required. The exact provider, tier, terms, retention, settings, and any credit-program override were recorded before use. The current Codex/ChatGPT account configuration remains unverified for raw-data processing, so no raw narrative or genome-scale value was exposed to it. The deterministic private GCP run completed; only organizer-permitted bounded findings and aggregate receipts were exported. Exact temporary resources must now be deleted and the teardown receipt recorded.

Point-by-point guidance source: https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/2 (comment timestamp `2026-08-26T22:28:34Z`).

## Hard gates before real-data execution

1. **Processor terms** — document provider, plan/tier, terms, no-training/no-rights language, retention period and purpose, exact settings, and any separate credit/grant terms. Do not rate or provide feedback on outputs containing challenge material.
2. **Storage** — at least 150 GB of approved encrypted working space, with backups and sync disabled unless explicitly covered by the data agreement.
3. **Isolation** — use only reviewed processor services; disable unnecessary telemetry, feedback, durable conversation state, file persistence, memory, public links, and third-party tools. Prevent patient content from entering shell history or captured task logs.
4. **Provenance** — record source hashes, tool versions, reference genome build, annotation versions, commands, and timestamps without copying patient-level values into the public receipt.
5. **Publication review** — manually inspect every public artifact for identifiers and patient-derived values before commit or upload.
6. **Deletion** — within 30 days after close, delete every participant-controlled VCF/BAM/CRAM copy, index, slice/reformat, genome-scale filtered/annotated genotype table, cache/notebook state containing it, stored prompt/log with pasted variant blocks, and model weight/embedding/fine-tune trained on raw genomic data. Confirm deletion manually and record the provider/configuration used.

## Organizer-confirmed keep versus delete boundary

May remain after manual publication review: the ranked candidate variant submission, HPO terms, gene/pathway rankings, mechanism analyses, drug candidates, code, report, pitch, and leaderboard entry.

Must be deleted: raw genomic files and indexes; copies, subsets, slices, or reformats; genome-scale per-variant genotype intermediates and caches; stored prompts containing blocks of variant data; and any weights, embeddings, or fine-tunes trained directly on raw genomic data. A small number of named variants is a finding; an artifact enabling reconstruction of a meaningful portion of the genome remains controlled data.

## Falsifiers and stop rules

- Any uncertainty about whether an artifact is a permitted finding or a reconstructive/genome-scale dataset stops export.
- Any network call from the real-data environment to an unreviewed provider stops the run.
- Any public artifact containing raw files, genome-scale genotypes, reconstructive intermediates, stored variant-block prompts, credentials, or unreviewed logs fails closed.
- No medication candidate is represented as treatment advice or clinical evidence.
