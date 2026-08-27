# MVA Hackathon 2026 — Track 1 report

> **DRAFT — DO NOT SUBMIT.** This public-safe scaffold contains no real patient data, candidate variants, or patient-derived phenotype terms. Replace bracketed fields only inside the approved private workflow, then perform the publication review defined in `docs/DATA_GOVERNANCE.md`.

## Submission identity

- Participant: `svillalobos-gonzalez` (solo)
- Model: `AxiomWeave MVA VCF-first baseline + challenger`
- Model number: `[ASSIGN AFTER MODEL FREEZE]`
- Repository: `[PUBLIC GITHUB URL AFTER PRIVACY REVIEW]`
- Source and evaluator freeze: see `docs/SOURCE_MANIFEST.md`

## Method abstract

We use a transparent, VCF-first rare-disease prioritisation workflow designed for an exact compound-heterozygous-pair submission. Structural checks and normalization precede phenotype-aware prioritisation with Exomiser 15.1.0 and its frozen 2602 GRCh38 and phenotype datasets. The baseline combines call quality, population rarity, functional consequence, recessive/compound-heterozygous inheritance, phenotype similarity, curated disease evidence, and segregation or phasing evidence when available. A pre-registered challenger uses Exomiser's documented exome-with-introns model to retain splice-relevant intronic candidates and treats known MVA mechanisms as a soft prioritisation feature rather than a hard gene-list exclusion. Candidate pairs remain together in one scored row. Phenotype-shuffle, phenotype-ablation, panel-ablation, frequency-order, and pair-ablation controls test whether the ranking depends on the claimed biological and scoring signals. Automated outputs undergo documented manual review of primary literature and disease-validity evidence before EPCR assignment. This design is reproducible and inexpensive, but it can miss causal events absent from or poorly represented in the supplied VCF; failed VCF sufficiency triggers a separately governed FASTQ reanalysis. A ranked challenge submission is a research hypothesis, not a diagnosis or medical recommendation.

## Inputs and data boundary

- Challenge input: gated GRCh38 VCF, index, and clinical/phenotype material accessed only in the approved private environment.
- Public repository: code, versions, schemas, synthetic fixtures, non-identifying receipts, and only the organizer-permitted findings that pass manual publication review.
- Hosted processors: allowed only after documenting no-training/no-rights terms, limited-purpose retention, provider/tier/settings, and any credit-specific overrides. Do not rate outputs containing challenge material.
- Explicit exclusions: no raw genomic files, indexes, genome-scale genotype tables, reconstructive intermediates, stored prompts containing blocks of variant data, or models trained on raw genomic data in public artifacts.
- Deletion: source, intermediate, and covered derived data will be removed within the organizer-required period and verified with a non-identifying receipt.

## Computational approach

1. Verify file hashes, reference build, sample count, genotype fields, index integrity, normalization status, and call-quality fields with `bcftools`/`tabix`.
2. Normalize only when required and preserve an immutable source copy inside the private environment.
3. Run the frozen Exomiser phenotype-driven baseline under recessive and compound-heterozygous inheritance models.
4. Run the official exome-with-introns challenger with splice-relevant intronic retention and a soft MVA mechanism prior, while preserving a phenotype-wide route.
5. Form candidate pairs explicitly and keep both variants in the same submission row.
6. Apply the frozen controls and retain failures rather than tuning them away.
7. Review the short list against primary literature, curated disease validity, population frequency, inheritance, segregation/phasing, and mechanism plausibility.
8. Freeze the candidate universe and EPCR mapping before replaying the pinned public evaluator.

## Manual review and curation

The final file will be computationally generated and then manually curated. Manual review may remove technically weak or biologically contradicted candidates, but every change must be recorded with its evidence, alternative, claim ceiling, falsifier, and reviewer decision. Manual review cannot introduce a candidate that was never present in an auditable upstream result without recording that deviation.

## Public and proprietary resources

The planned baseline uses publicly documented Exomiser software and the frozen 2602 datasets, including Ensembl 112/MANE, gnomAD 4.1, ClinVar dated 2026-02-08, HPO, OMIM, Orphanet, and other sources documented by the Exomiser release. Primary literature and curated gene-disease resources are used for candidate-specific review. No proprietary patient or comparator dataset is planned. Any externally licensed annotation source will be disclosed, and its database files will not be redistributed.

## Compound-heterozygous output

The approach explicitly forms and ranks proposed compound-heterozygous pairs. Both variants are emitted together in one CSV row. Phase or segregation is treated as evidence when available and as an uncertainty when unavailable; it is not silently assumed.

## Secondary/incidental findings

The scored CSV defaults to primary causal hypotheses only. Broader incidental analysis belongs in the report unless the organizer resolves the current discrepancy between the FAQ and the public evaluator. Any secondary row must be placed below primary candidates and replayed locally because the pinned evaluator currently includes it in rank and F-max calculations.

## Candidate evidence table

No real-data result exists yet. Populate this table only after the private run and publication review.

| Rank | Candidate pair | Gene/mechanism | Inheritance/phase | Phenotype evidence | Population/functional evidence | EPCR | Main falsifier |
|---:|---|---|---|---|---|---:|---|
| `[1]` | `[PRIVATE UNTIL CLEARED]` | `[PENDING]` | `[PENDING]` | `[PENDING]` | `[PENDING]` | `[PENDING]` | `[PENDING]` |

## Negative controls and sensitivity checks

- Phenotype shuffle: a phenotype-driven ranking should materially degrade.
- Phenotype ablation: the full model must add evidence beyond a no-HPO run.
- Frequency ordering: the full model must add evidence beyond a population-frequency-only ordering derived from reported frequency fields.
- Panel ablation: a candidate that survives only a narrow MVA panel is labelled panel-dependent.
- Pair ablation: splitting a pair must reproduce the expected scorer penalty.
- VCF sufficiency: missing genotype/call fields, QC failure, or no defensible pair triggers a separately approved FASTQ decision.

## Runtime and cost

Public synthetic preflight completed on an ephemeral 8-vCPU/32-GB GCP VM in 31 seconds for the minimal Exomiser example. That is infrastructure evidence only. Record the real VCF runtime, peak storage, and actual cloud cost here after the private run: `[PENDING]`. The first private compute window is limited to six hours, is expected to remain below USD 10, and may not exceed the separately approved USD 20 owner ceiling.

## Strengths and limitations

Strengths include transparent scoring alignment, explicit pair formation, phenotype-wide and MVA-aware routes, negative controls, versioned sources, and an auditable privacy boundary. Limitations include dependence on the supplied VCF, incomplete sensitivity for structural/non-coding events, uncertain phasing or segregation when family data are absent, annotation-version dependence, and the absence of clinical validation. Leaderboard agreement would remain observational challenge evidence rather than a diagnosis.

## Final pre-submission receipt

- [ ] Candidate list frozen and evidence cards complete.
- [ ] CSV passes `scripts/validate_track1_submission.py`.
- [ ] Exact pinned evaluator replayed locally.
- [ ] Report contains no prohibited patient-derived material.
- [ ] Public repository works while logged out and contains no secrets or gated files.
- [ ] Team/display name and filename match registration.
- [ ] Live attempt number and purpose are recorded before submission.
- [ ] User approves the final irreversible submission click.
