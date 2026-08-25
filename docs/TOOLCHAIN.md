# Frozen public toolchain

Access date: 2026-08-25.

## Selected baseline

| Component | Version/data | Role | Evidence ceiling |
|---|---|---|---|
| Exomiser CLI | 15.1.0 | open phenotype/variant prioritisation baseline | public software smoke test only until real-data run |
| Exomiser data | 2602, GRCh38 plus phenotype | Ensembl 112/MANE, gnomAD 4.1, ClinVar 2026-02-08, HPO/OMIM/Orphanet and other documented sources | annotation inputs, not independent truth |
| Java | OpenJDK 21.0.12 on the ephemeral VM | Exomiser runtime | infrastructure receipt |
| bcftools/tabix | 1.19 | VCF structure, normalization, indexing and query checks | structural/QC evidence only |
| Official challenge evaluator | pinned hash in `SOURCE_MANIFEST.md` | exact local scoring replay | C1 synthetic mechanics |

Exomiser 15.1.0 was the latest non-prerelease GitHub release returned by the official release API at freeze time. Its official distribution asset is 170,449,958 bytes with publisher-reported SHA-256 `47faa54d4791686c9dc3f896762834630e9eaf607ad3cf3399074353c3dda248`.

The selected 2602 archives are:

- `2602_hg38.zip`: 23,576,028,714 bytes by authoritative CDN response;
- `2602_phenotype.zip`: 13,478,530,504 bytes by authoritative CDN response.

The run records locally computed archive hashes after transfer. The publisher did not expose companion checksum files at the probed paths, so those local hashes prove later byte identity only; they are not an independent publisher-integrity proof.

## Why this baseline

The CAGI6 Rare Genomes assessment found no universal winner, but open Exomiser was among the strong general approaches and the benchmark favored combining call quality, rarity, predicted impact, inheritance, phenotype similarity, and disease knowledge. This directly matches the challenge scorer's need to rank one exact compound-heterozygous pair while remaining auditable.

## Challenger additions

- non-coding and splice retention rather than an exome-only hard filter;
- the frozen MVA core/no-miss mechanism universe in `DECISION_PACKET.md`;
- explicit pair formation, phasing/segregation evidence, and evaluator-aware output formatting;
- negative controls that remove phenotype or panel information.

VEP 116 was inspected as a current alternative, but it was not selected for the first smoke run because Exomiser already bundles the phenotype-driven baseline and adding a second large annotation stack would increase storage, versioning, and integration risk without answering a new first-pass question.

## Licensing and publication gate

Exomiser software and its downloaded databases do not share one universal license. The 2602 release notes specifically warn that SpliceAI annotations have academic/not-for-profit terms and separate commercial-use requirements. Do not redistribute the databases. Before publishing the final repository or using the outputs beyond this research challenge, review the licenses for every enabled source and either document compatibility or disable/replace the source.

## Falsifiers

- If the official public smoke example fails on the pinned runtime/data, the baseline remains unavailable until the failure is reproduced and resolved.
- If the VCF lacks sample/genotype fields required for inheritance analysis, Exomiser alone is insufficient.
- If phenotype shuffling leaves rankings materially unchanged, the phenotype-driven claim is rejected.
- If a candidate appears only under a narrow gene boost and disappears in the phenotype-wide run, label it panel-dependent rather than robust.
