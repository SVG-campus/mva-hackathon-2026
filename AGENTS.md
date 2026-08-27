# MVA Hackathon Project Instructions

This project supports the 2026 SageBio "Rare Disease, Real Kid" MVA Hackathon.

## Non-negotiable data boundary

- The challenge data describe a real child. Never place raw, genome-scale, reconstructive, or otherwise prohibited patient material in a public repository or an unreviewed hosted service. Only organizer-permitted findings may be published after manual review, and only services with a dated `PASS_PROCESSOR` record may process gated material.
- Before any hosted service processes gated or patient-derived material, record the provider, plan/tier, applicable terms, retention period/purpose, and exact settings. The service must take no rights in inputs or outputs, perform no training on them, and retain content only for a limited operational purpose. Do not rate outputs or submit feedback containing challenge material.
- Public code may contain schemas, synthetic fixtures, non-identifying receipts, and manually reviewed research findings permitted by the organizers, including a short ranked candidate list and HPO/gene/pathway analyses. It must not contain raw genomic files, genome-scale genotype tables, slices/reformats, annotated variant tables, notebook state, stored prompts with blocks of variant data, trained weights/embeddings from raw genomic data, or anything enabling reconstruction of a meaningful portion of the child's genome.
- Do not search for or use public family stories to re-identify the child or infer the hidden answer key.
- Keep the official 30-day post-close deletion and confirmation requirement as a fail-closed release gate. Delete controlled copies of VCF/BAM/CRAM data, indexes, genome-scale intermediates, caches/notebook state, stored prompts containing variant blocks, and models trained on raw genomic data. Provider logs outside the participant's control are governed by the documented processor terms.

## Action boundary

- Local read-only research, synthetic tests, and reversible code edits are allowed.
- Submissions, outreach, account changes, public repository creation/push, video upload, cloud compute, and spend require explicit user authorization.
- Do not consume any of the six Track 1 attempts or the single Track 2 attempt during development.
- For this project, use only the owner-selected default Google Cloud project and account recorded in ignored `private_state/`. Verify both before every mutating command. Isolate hackathon resources by the frozen `mva-` names; never read, modify, move, or delete pre-existing unrelated resources in that shared project.

## Evidence rules

- Apply the AxiomWeave packet fields to every material decision: question, assumptions, options, evidence, decision, C0-C6 ceiling, falsifier, budget, and stop rule.
- Preliminary synthetic or evaluator-mechanics tests are capped at C1. A candidate ranking is not a diagnosis; a drug hypothesis is not treatment evidence or medical advice.
- Preserve failed tests and negative controls. Freeze scoring rules, seeds, source versions, and candidate universes before claim-bearing runs.
- Use the official challenge source commit and file hashes recorded in `docs/SOURCE_MANIFEST.md`.
