# MVA Hackathon 2026 — Track 1 report

## Submission identity

- Participant: `svillalobos-gonzalez` (solo)
- Model: `AxiomWeave MVA VCF-first baseline + intronic challenger`
- Model number: 1
- Repository: `https://github.com/SVG-campus/mva-hackathon-2026` (to be activated after final privacy review)
- Prediction file: `svillalobos-gonzalez_model1_bub1b_predictions.csv`

## Abstract

This submission uses a transparent VCF-first workflow designed for the challenge's exact compound-heterozygous-pair evaluator. It performs fail-closed GRCh38/sample/genotype checks, phenotype-aware prioritization with Exomiser 15.1.0 and the frozen 2602 datasets, an official exome-with-introns challenger, explicit pair formation, phenotype-ablation and phenotype-shuffle controls, rarity-only comparison, and manual review against primary and curated sources. The final scored CSV contains one BUB1B pair. The result is a challenge research hypothesis, not a diagnosis or medical recommendation.

## Data and governance boundary

The gated VCF, index, and phenotype document were accessed only on an isolated, IAP-only Google Compute Engine VM in the participant-selected project. The VM had no service account, no public application endpoint, no snapshots, and a six-hour automatic deletion limit. No raw genomic file, clinical narrative, genome-scale table, prompt containing blocks of variant data, or model trained on raw challenge data is published. Only the organizer-permitted short finding, HPO terms, methods, and non-identifying aggregate receipts were retained for review. Covered private cloud artifacts are deleted after reduction and verified separately.

## Input quality checks

- Repository metadata and hashes were recorded for one VCF, one tabix index, and one phenotype document; total download size was 317,514,212 bytes.
- The VCF was confirmed as GRCh38 with exactly one sample and readable indexed records.
- GT, DP, and GQ fields were present.
- Eight explicit HPO identifiers were found and converted to a local phenopacket.
- The structural validator and 20 local tests passed.

## Computational approach

1. Validate source sizes/hashes, VCF header/build, sample count, index readability, genotype fields, and HPO identifiers.
2. Run Exomiser 15.1.0 with frozen 2602 GRCh38/phenotype resources using its exome preset.
3. Run the official exome-with-introns preset as a challenger.
4. Run phenotype ablation with the HPO ontology root and a fixed unrelated-phenotype shuffle.
5. Derive a true rarity-only ordering from population-frequency fields.
6. Form exact two-variant autosomal-recessive gene pairs and combine route consistency, phenotype specificity, rarity, and an MVA mechanism tier.
7. Manually remove technically/biologically weak pairs and review the lead against ClinGen, ClinVar, UniProt, Orphanet, and primary literature.
8. Validate the frozen CSV and replay the pinned public evaluator under the candidate-as-truth sensitivity check.

## Phenotype features used

`HP:0000121` Nephrocalcinosis; `HP:0001508` Failure to thrive; `HP:0001518` Small for gestational age; `HP:0001622` Premature birth; `HP:0002859` Rhabdomyosarcoma; `HP:0003202` Skeletal muscle atrophy; `HP:0004322` Short stature; `HP:0200067` Recurrent spontaneous abortion.

## Submitted candidate

| Rank | Pair (GRCh38) | Gene / mechanism | Technical evidence | Phenotype/control evidence | EPCR |
|---:|---|---|---|---|---:|
| 1 | `chr15:40209701 T>G` + `chr15:40220612 T>G` | BUB1B; proposed AR compound heterozygosity | Both PASS, `0/1`, GQ 99; DP/AD 46/21,25 and 28/15,13 | Baseline rank 2; intronic rank 2; ablation rank 5; shuffle rank 6; rarity-only rank 27 | 0.46916 |

The first allele is `NM_001211.6:c.2210T>G (p.Leu737Ter)`, a stop-gained variant classified pathogenic in ClinVar. The second is `c.3006T>G (p.Asn1002Lys)`, an uncatalogued rare missense call classified as a VUS by the frozen Exomiser evidence. UniProt places residue 1002 inside the BUB1B protein-kinase domain (766–1050). ClinGen classifies BUB1B–MVA1 as a definitive autosomal-recessive relationship and specifically recognizes null-plus-missense/hypomorphic compound heterozygosity as a disease mechanism. The HPO profile contains prenatal growth restriction/short stature and rhabdomyosarcoma, features described in BUB1B-related MVA literature.

Direct sources: [ClinGen BUB1B–MVA1](https://search.clinicalgenome.org/kb/gene-validity/CGGV%3Aassertion_59147f27-d5a3-4760-ba8d-0429bae3c906-2019-11-22T14%3A53%3A26.352Z), [ClinVar p.Leu737Ter](https://www.ncbi.nlm.nih.gov/clinvar/RCV000641226/), [UniProt O60566](https://www.uniprot.org/uniprotkb/O60566/entry), [Hanks et al. 2004](https://pubmed.ncbi.nlm.nih.gov/15475955/), and [Orphanet ORPHA:1052](https://www.orpha.net/en/disease/detail/1052).

## Negative controls and adjudication

The BUB1B pair fell from rank 2 to rank 5 under phenotype ablation, rank 6 with unrelated HPO terms, and rank 27 under rarity-only ordering. This supports dependence on phenotype/disease information rather than rarity alone, but it is not independent validation. Several lower computational pairs were adjacent or common and were excluded from the conservative Model 1 CSV. Under a hypothetical replay in which the submitted pair is the hidden answer, the pinned evaluator returns rank points 100 and F-max 1.0; this is a mechanics test, not evidence that the hidden answer is known.

## Runtime and resources

Successful route runtimes were 142 seconds (baseline exome), 360 seconds (intronic challenger), 111 seconds (phenotype ablation), and 148 seconds (phenotype shuffle), totaling 761 seconds. At the final measurement, the public Exomiser toolchain occupied 58.65 GB, the private workspace 0.34 GB, and the 200-GB root disk used 61.84 GB. These are end-of-run, not peak, storage measurements. The job used one `e2-standard-8` VM and remained within the approved USD 20 ceiling; final provider billing may lag.

## Strengths and limitations

Strengths are exact-pair scorer alignment, reproducible public code, phenotype-wide analysis, an intronic challenger, explicit negative controls, bounded manual review, and an auditable deletion boundary. The decisive limitations are that the two variants are unphased, the missense partner is a VUS without direct functional evidence, and the supplied VCF may miss structural/non-coding events. Parental or read-backed phasing that places both variants in cis would falsify the compound-heterozygous claim. Leaderboard agreement would remain observational challenge evidence rather than clinical validation.

## Reproducibility receipt

- CSV schema validation: PASS, 1 row.
- Local test suite: PASS, 20 tests.
- Candidate-as-truth evaluator replay: rank points 100, F-max 1.0 (hypothetical mechanics check only).
- Prediction SHA-256: `B4BA215877DA41C84480A2D8D389BC9BEDE527577A8A0287F97E0A874CEBCFE9`.
- Source/evaluator hashes and public provenance are frozen in `docs/SOURCE_MANIFEST.md`.

Claim ceiling: C2 observational challenge hypothesis. No clinical, diagnostic, therapeutic, or winning-probability claim is made.
