# Organizer questions requiring human submission

No message has been sent from this project. The user should post or email these questions manually, without including patient-level information.

## Resolved 2026-08-26 — hosted processors and deletion

Sage's Chief Privacy and Compliance Officer supplied the promised point-by-point answer. A hosted service may act as a processor when it takes no rights in inputs or outputs, performs no training, and retains material only for a limited operational purpose. Zero retention and local inference are not required. Participants must inspect the exact provider, plan/tier, settings, retention, and any credit-program terms, and must not rate outputs containing challenge material. The answer also defines which findings may remain and which genome-bearing artifacts must be deleted. The operational interpretation is frozen in `docs/DATA_GOVERNANCE.md` and `docs/PROVIDER_TERMS_CHECKLIST.md`.

Discussion: https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/2

## Priority 1 — scorer/documentation discrepancy

> The FAQ says secondary/incidental findings will not hurt automated scoring, but the current public evaluator appears to rank and threshold all rows without filtering `finding_type`. Can you confirm whether participants should expect secondary rows to affect rank and F-max, and whether the deployed evaluator will change?

## Resolved — derived-data publication versus deletion

The organizer permits a short ranked candidate list, HPO terms, gene/pathway rankings, mechanism analyses, drug candidates, code, report, pitch, and leaderboard entry to remain. Raw genomic files and indexes, slices/reformats, genome-scale genotype intermediates and caches, stored prompts containing blocks of variant data, and models trained on raw genomic data must be deleted. See `docs/DATA_GOVERNANCE.md` for the reconstruction boundary.

## Priority 3 — prize allocation

> Are the listed first, second, third, and innovation awards selected across both tracks combined, or is there a separate award set for each track?

## Priority 4 — Track 2 medication scope

> For Track 2, does “approved existing medication” mean FDA-approved, approved by any stringent regulatory authority, or approved anywhere? Are pediatric formulation, route, and exposure feasibility required in the submission?

## Stop rule

Do not repeat a resolved question. Re-open the privacy thread only if a specific provider term or workflow creates a new material ambiguity that cannot be resolved from the written answer.
