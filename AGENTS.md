# MVA Hackathon Project Instructions

This project supports the 2026 SageBio "Rare Disease, Real Kid" MVA Hackathon.

## Non-negotiable data boundary

- The challenge data describe a real child. Never commit, paste, upload, summarize, or expose individual-level genomic or clinical content to a public repository or a hosted AI/API service.
- Until the organizers answer the public third-party-LLM/data-handling question, treat all gated source data and derived patient-specific artifacts as local-only and unavailable to agents.
- Public code may contain schemas, synthetic fixtures, and aggregate non-identifying receipts only. It must not contain real coordinates, alleles, HPO terms, screenshots, logs, candidate lists, or prompts derived from the child.
- Do not search for or use public family stories to re-identify the child or infer the hidden answer key.
- Keep the official 30-day post-close deletion and confirmation requirement as a fail-closed release gate.

## Action boundary

- Local read-only research, synthetic tests, and reversible code edits are allowed.
- Submissions, outreach, account changes, public repository creation/push, video upload, cloud compute, and spend require explicit user authorization.
- Do not consume any of the six Track 1 attempts or the single Track 2 attempt during development.

## Evidence rules

- Apply the AxiomWeave packet fields to every material decision: question, assumptions, options, evidence, decision, C0-C6 ceiling, falsifier, budget, and stop rule.
- Preliminary synthetic or evaluator-mechanics tests are capped at C1. A candidate ranking is not a diagnosis; a drug hypothesis is not treatment evidence or medical advice.
- Preserve failed tests and negative controls. Freeze scoring rules, seeds, source versions, and candidate universes before claim-bearing runs.
- Use the official challenge source commit and file hashes recorded in `docs/SOURCE_MANIFEST.md`.
