# Preliminary route decision — 2026-08-25

## Decision question

Which submission route gives this team the best evidence-governed chance of a strong hackathon result while protecting the real child, preserving scarce live attempts, and staying executable before 2026-10-24 23:59 UTC?

## Frozen assumptions

1. The public challenge source and evaluator at the commits in `SOURCE_MANIFEST.md` remain authoritative until a later commit is detected.
2. The supplied VCF is GRCh38 and contains enough information to test a variant-first route; this is a hypothesis, not an established fact.
3. The answer is one exact compound-heterozygous pair, as encoded in the public evaluator.
4. Real patient data and patient-derived artifacts remain outside hosted AI/API systems until the organizer resolves the public data-handling question.
5. A drug proposal is not a treatment recommendation. It must be downstream of a supported causal mechanism.

## Objective lenses and hard gates

The route is judged on competition fit (25%), evidence strength (20%), differentiation (20%), execution by the deadline (15%), privacy/governance (15%), and future option value (5%). Scores below are ordinal planning aids, not probabilities of winning.

Hard gates override every score:

- no real-data handling without accepted dataset terms, an isolated compute path, and an auditable deletion plan;
- no live submission until the candidate list and report are frozen and replayed against the pinned evaluator;
- no Track 2 recommendation without a causal gene/variant mechanism, approved-drug status, dose/exposure plausibility, and explicit contraindication review;
- abstain if no candidate survives the evidence thresholds.

## Alternatives

| Route | Weighted planning score / 5 | Current ceiling | Main advantage | Decisive weakness |
|---|---:|---|---|---|
| Abstain from real-data work for now | 3.30 | C0 | Safest negative control and preserves all attempts | Cannot produce a competitive result by itself |
| Track 1, VCF-first | **4.50** | C1 mechanics; C0 biological route | Fast, cheap, aligned to exact scorer, highly reproducible | Can miss variants absent or poorly represented in the VCF |
| Track 1, FASTQ reanalysis first | 3.80 | C0 | Can recover calling and structural/non-coding misses | About 85 GB transfer, larger annotation footprint, and much more execution risk |
| Track 2 immediately | 3.10 | C0 | Panel judging rewards innovation and impact | The causal mechanism is unknown and no established disease-modifying approved drug was found |
| Track 1 first, then gated Track 2 bridge | 4.10 | C0 program hypothesis | Preserves both tracks and turns a diagnostic result into a mechanism-specific proposal | More work; Track 2 remains invalid if Track 1 does not establish a usable mechanism |

## Selected route

**Develop Track 1 VCF-first now; preserve Track 2 as a contingent extension.**

The end-state is an integrated diagnostic-to-mechanism story, but the first claim-bearing run is Track 1 only. Start with a transparent baseline and a pre-registered challenger:

### Baseline

- require defensible call quality;
- rank rare variants under recessive and compound-heterozygous inheritance;
- combine population frequency, predicted functional consequence, ClinVar/curated disease evidence, phenotype similarity, and segregation or phasing evidence when present;
- output pairs together in a single scored row;
- reserve high EPCR values for primary candidates only.

### Challenger

- retain splice-region, intronic, regulatory, and other non-coding candidates instead of hard-filtering them away;
- search the seven numbered forms as the high-priority core: `BUB1B`, `CEP57`, `TRIP13`, `CENATAC`, `SMC5`, `SLF2`, and `MAD1L1`;
- add `BUB1`, `MAD2L1BP`, and `CEP192` as lower-maturity no-miss genes;
- do not allow the panel to become a hard gene-list exclusion: phenotype-wide ranking remains the negative control.

## Evidence packet

| Evidence | Layer | What it supports | What it does not support |
|---|---|---|---|
| Official public source, templates, rules, and evaluator | primary challenge evidence | mechanics, fields, limits, deadlines, scoring behavior | identity of the real causal pair or future rule stability |
| Six synthetic evaluator tests | local synthetic verification | pair-row, rank-tier, EPCR, row-limit, and secondary-row behavior | real-data accuracy or leaderboard performance |
| CAGI6 Rare Genomes assessment | peer-reviewed benchmark | value of call quality, rarity, inheritance, phenotype and disease evidence; competitive open-source baseline | performance on this child |
| MVA reviews, ClinGen, and primary gene reports | curated/peer-reviewed scientific evidence | bounded gene/mechanism universe and need to retain non-coding/splice candidates | that any one gene is causal here |
| Cell rescue studies for BUBR1 and TRIP13 | primary mechanistic evidence | protein restoration can rescue cellular checkpoint defects in those specific models | efficacy of an approved drug in this child |

## Negative controls and falsifiers

1. **Phenotype shuffle:** randomize or replace phenotype terms. A purportedly phenotype-driven ranking should materially degrade.
2. **Frequency-only baseline:** the full model must beat a ranking based only on rarity under frozen evaluation criteria.
3. **Panel ablation:** run phenotype-wide ranking without an MVA gene boost. If the candidate vanishes solely because the panel was removed, label it panel-dependent.
4. **Pair ablation:** split paired variants across rows to verify the exact expected scorer penalty.
5. **VCF sufficiency falsifier:** escalate to FASTQ only if the VCF lacks needed genotype/call fields, shows QC failure, or produces no defensible pair after the frozen pipeline.
6. **Track 2 falsifier:** stop Track 2 if mechanism direction, tissue relevance, approved-drug exposure, or a decisive safety conflict cannot be supported.

## Claim ceiling

Current overall ceiling: **C1 for scorer mechanics and synthetic infrastructure; C0 for causal-gene, variant, drug, and winning-route hypotheses.** A leaderboard score would be observational challenge evidence, not a diagnosis or clinical validation.

## Budgets and stop rules

- Live Track 1 attempts: six total; development budget **zero**. Proposed allocation after freeze: one smoke submission, two planned model comparisons, one calibrated improvement, and two held in reserve.
- Track 2 attempts: one total; use only after the mechanism gate.
- Cloud first-run budget: expected under USD 10 and hard owner approval ceiling USD 20; the Console estimate must be reviewed immediately before creation. A billing budget is an alert, not a hard cap.
- First compute window: six hours, no GPU, automatic VM and boot-disk deletion.
- FASTQ escalation: only after the VCF sufficiency falsifier fires and a separate storage/cost plan is approved.
- Diminishing-returns stop: freeze when two consecutive pre-registered changes fail to improve the same offline evidence rubric or when only untestable narrative changes remain.
