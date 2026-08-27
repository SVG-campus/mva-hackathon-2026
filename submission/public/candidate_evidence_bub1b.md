# Candidate-pair evidence card — BUB1B

## Identity and computational provenance

- Submission rank: 1
- Pair: GRCh38 `chr15:40209701 T>G` and `chr15:40220612 T>G`
- Gene / proposed mechanism: `BUB1B`; proposed autosomal-recessive compound heterozygosity for mosaic variegated aneuploidy syndrome 1
- Baseline Exomiser rank: 2
- Exome-with-introns rank: 2
- Phenotype-ablation rank: 5
- Phenotype-shuffle rank: 6
- Frequency-only rank: 27
- Soft MVA prior tier: `core_mva`

## Technical evidence

| Check | Evidence | Decision ceiling | Falsifier |
|---|---|---|---|
| VCF representation | Two distinct GRCh38 SNVs approximately 10.9 kb apart; both `PASS` | C1 structural | Reference/alternate mismatch or normalization conflict |
| Genotype and call quality | Both `0/1`, GQ 99; depth/allele depth 46/21,25 and 28/15,13 | C1 technical | Read-level artifact, mapping artifact, or orthogonal validation failure |
| Recessive pair formation | Two qualifying heterozygous variants in the same gene | C1 computational | Variants are shown to be in cis |
| Phase / segregation | No PS, PID, or PGT fields were present for this pair; trans phase is not established | C0 for phase | Parental/read-backed phasing places both alleles in cis |

## Biological evidence

| Check | Evidence and source | Decision ceiling | Falsifier |
|---|---|---|---|
| Population frequency | Exomiser 2602 reports maximum population frequencies of 0.00998214% and 0.00008992758%; annotation is version-dependent | C1 annotation | A reliable population source shows frequency incompatible with rare recessive disease |
| Functional consequence | `c.2210T>G p.Leu737Ter` is stop-gained; `c.3006T>G p.Asn1002Lys` is missense. UniProt places residue 1002 within the reviewed BUB1B protein-kinase domain (766–1050). | C1–C2 | Benign functional evidence or transcript mismatch |
| ClinVar | The stop allele is pathogenic in ClinVar, current record RCV000641226. The exact missense allele was not supplied by ClinVar in the frozen Exomiser data and remains a VUS. | C1–C2 | Expert benign classification or conflicting validated transcript mapping |
| Gene–disease validity | ClinGen classifies BUB1B–MVA1 as definitive, autosomal recessive, and describes null-plus-missense/hypomorphic compound heterozygosity as an established mechanism. | C2 | Revised/disputed validity or incompatible inheritance |
| Phenotype fit | Eight explicit HPO terms included prenatal growth restriction, failure to thrive, short stature, and rhabdomyosarcoma. Orphanet and the original BUB1B report describe prenatal growth retardation and childhood cancer, including rhabdomyosarcoma. | C2 observational | Independent phenotype review favors another syndrome or the ranking survives all phenotype controls unchanged |
| Controls | Rank changed from 2 to 5 under phenotype ablation, 6 under shuffled HPO, and 27 under rarity-only ordering; phenotype-specificity delta 0.3688 | C2 observational | Reimplementation fails to reproduce the control ordering |

## Direct sources

- ClinGen gene–disease validity: https://search.clinicalgenome.org/kb/gene-validity/CGGV%3Aassertion_59147f27-d5a3-4760-ba8d-0429bae3c906-2019-11-22T14%3A53%3A26.352Z
- ClinVar p.Leu737Ter: https://www.ncbi.nlm.nih.gov/clinvar/RCV000641226/
- UniProt BUB1B (O60566): https://www.uniprot.org/uniprotkb/O60566/entry
- Original BUB1B/MVA report: https://pubmed.ncbi.nlm.nih.gov/15475955/
- Orphanet MVA syndrome: https://www.orpha.net/en/disease/detail/1052

## Decision

- Disposition: retain as the sole Model 1 scored pair.
- EPCR: `0.46916`, a deterministic route-ranking proxy rather than a calibrated clinical probability.
- Main uncertainty: the missense allele is a VUS and trans phase is not established.
- Decisive next check: parental or read-backed phasing plus functional/clinical evidence for p.Asn1002Lys.
- Reviewer: `svillalobos-gonzalez` with Codex-assisted evidence synthesis, 2026-08-27.

Claim ceiling: C2 observational challenge hypothesis. This is not a diagnosis, clinical validation, treatment recommendation, or estimate of personal outcome.
