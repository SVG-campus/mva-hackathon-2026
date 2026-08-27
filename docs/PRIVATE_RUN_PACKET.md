# Private Track 1 run packet — frozen 2026-08-27

## Question

Can the supplied gated VCF support a defensible ranked compound-heterozygous Track 1 submission under the official scorer, privacy rules, and the owner-approved cloud budget?

## Assumptions and unknowns

- Dataset terms are accepted and the authenticated account is authorized to access the gated files.
- The VCF is GRCh38 and exposes usable sample, genotype, call-quality, and inheritance fields; this remains unverified until private QC.
- The public evaluator and submission schema frozen in `SOURCE_MANIFEST.md` remain current.
- Google Cloud Compute Engine/Persistent Disk is used only through isolated, exactly named `mva-` resources in the owner-selected free-credit project. Pre-existing buckets and unrelated resources remain untouched. No patient content enters Codex, GitHub, Kaggle, Vertex AI, hosted notebooks, MCP servers, support tickets, feedback, or an unreviewed API.
- Family structure, phasing, coverage, and structural/non-coding sensitivity may be incomplete.

## Alternatives

1. **Selected baseline:** private VCF-first Exomiser analysis with explicit compound-heterozygous pair formation.
2. **Challenger:** use Exomiser's official `preset-exome-analysis-with-introns.yml` to retain splice-relevant intronic candidates, then apply the MVA mechanism set only as a soft feature rather than a hard exclusion. A full Genomiser run is out of scope for this first window because its REMM dependency is not installed.
3. **Escalation:** FASTQ reanalysis only if the VCF sufficiency falsifier fails and a new storage/cost packet is approved.
4. **Abstention:** do not consume a live attempt if no candidate pair survives technical, inheritance, disease-validity, and privacy review.

## Evidence and provenance

- Official challenge source, evaluator, templates, and hashes: `SOURCE_MANIFEST.md`.
- Organizer processor/deletion answer: discussion #2, timestamp `2026-08-26T22:28:34Z`.
- GCP public synthetic receipt: `PUBLIC_PREFLIGHT_RECEIPT.md`.
- Provider decision: `PROVIDER_TERMS_CHECKLIST.md`.
- Local structural suite: 20 tests passed after the private intake, local HPO-mapping fallback, control, and compound-pair shortlist gates were added.

## Decision

Create one isolated ephemeral GCP VM in the exact owner-selected project/account, retrieve only the VCF/index/phenotype inputs, run frozen QC and Exomiser routes, execute negative controls, and export only a short manually reviewed finding set. Keep all live attempts unconsumed until the candidate universe, EPCR mapping, report, and evaluator replay are frozen.

## Claim ceiling

- Infrastructure and schema before the private run: **C1**.
- Candidate ranking from this single challenge case: at most **C2 observational evidence**.
- No output is a diagnosis, clinical validation, treatment recommendation, or winning probability.

## Retained execution failure

- The first private QC invocation used a nonexistent `bcftools quickcheck` subcommand and therefore failed before inspecting variant records. The downloaded files matched their repository metadata and hashes. The guard was replaced with explicit repository-size equality, `bcftools view --header-only`, indexed-record, GRCh38, sample, and genotype checks; the failed marker is retained in the execution history rather than counted as a biological failure.
- The supplied tabix index returned zero for `bcftools index --nrecords`; treating that metadata value as proof of an empty VCF caused the second fail-closed stop. The retry uses a bounded stream-presence test that reads only the first record inside the VM and emits only a boolean lower-bound receipt. No variant value is printed or transmitted.
- The first Exomiser baseline start failed because the public `2602_hg38` and `2602_phenotype` archive roots preserved owner-only directory modes. The earlier synthetic smoke ran under `sudo`, so it did not expose the mismatch. Repair is limited to `a+rX` on the public Exomiser installation; private input and result directories remain mode `0700`, and the failed output/log are moved to the private failure archive.

## Falsifiers and negative controls

- Stop if the VCF build, sample, genotype, call-quality, or indexing checks fail.
- Prefer explicit HPO identifiers. If absent, permit only unambiguous exact HPO names/synonyms mapped locally against the frozen public ontology; reject negated terms and retain the short mapping for review.
- Stop if a command would print, transmit, or persist a genome-scale table outside the private VM.
- Phenotype-shuffle, phenotype-ablation, panel-ablation, and pair-ablation controls must remain in the receipt even when unfavorable. A true frequency-only ordering is derived separately from reported population-frequency fields; removing HPO terms alone is not labelled frequency-only.
- Abstain if no candidate pair survives rarity, quality, inheritance, disease-validity, and literature review.
- A changed evaluator, schema, dataset manifest, or source commit invalidates the frozen replay.

## Budget and stop rules

- One `e2-standard-8` VM, 200 GB balanced auto-delete disk, maximum six hours.
- Expected first-run cost below USD 10; owner-approved hard decision ceiling USD 20. A budget alert is monitoring, not a cap.
- VM auto-deletes at six hours; delete sooner after outputs are reduced to permitted findings.
- Do not create snapshots, custom images, persistent buckets, service-account credentials, or extra hosted services.
- Submission proceeds only after structural validation, local scorer replay, privacy review, and a frozen evidence card; otherwise preserve all attempts.
