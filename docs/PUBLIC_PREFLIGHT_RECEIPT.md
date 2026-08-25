# Public toolchain preflight receipt

Run date: 2026-08-25. Scope: public software, public annotation databases, and a synthetic two-record GRCh38 fixture only. No gated challenge file, Hugging Face token, or patient-derived content entered the environment.

## Environment

- ephemeral GCP VM: 8 vCPU, 32 GB RAM, 200 GB balanced disk;
- OpenJDK 21.0.12;
- bcftools/tabix 1.19;
- Exomiser CLI 15.1.0;
- Exomiser 2602 GRCh38 and phenotype data;
- maximum lifetime six hours with automatic instance/disk deletion;
- no VM service account or API scopes; Shielded VM enabled; SSH restricted to IAP.

## Integrity receipt

| Archive | Bytes | SHA-256 | Integrity interpretation |
|---|---:|---|---|
| `exomiser-cli-15.1.0-distribution.zip` | 170,449,958 | `47faa54d4791686c9dc3f896762834630e9eaf607ad3cf3399074353c3dda248` | matches publisher GitHub digest |
| `2602_hg38.zip` | 23,576,028,714 | `2ed14f8b63b5612068591648d8c3c6e34ce9d1c66c08a78990597f78031df447` | locally frozen transfer hash; publisher checksum unavailable at probed path |
| `2602_phenotype.zip` | 13,478,530,504 | `aa923530ca43cf5051ed2ba7b221bb73deb2b0dd66695b2ba60460db052f0493` | locally frozen transfer hash; publisher checksum unavailable at probed path |

Installed footprint: 55 GB. Free disk after installation: 136 GB.

## Retained failures

1. **Mutable installer path:** overwriting a script path while its first process was still reading it caused extraction to stop after the complete downloads. No archive was modified. Repair: immutable `v2` path plus exact-size gates and publisher hash verification.
2. **Missing sample:** the first Exomiser invocation correctly rejected the VCF with `No sample specified!`. Repair: add a v1 synthetic phenopacket whose subject ID matches the VCF sample.
3. **Unwanted default assembly:** the distribution defaults enabled hg19/2512 and failed because only hg38 was intentionally downloaded. Repair: a run-specific properties file enabling only hg38/2602 and phenotype/2602.

These failures are part of the reproducibility evidence. They are not hidden or counted as successful analyses.

## Passing synthetic smoke

- input: one synthetic sample, two arbitrary/intergenic GRCh38 SNVs;
- Exomiser runtime: 31 seconds;
- databases opened: `2602_hg38_genome` and `2602_phenotype`;
- output files: HTML, JSONL, and Parquet;
- result count: zero genes/variants after effect filtering, expected because the coordinates were deliberately arbitrary and non-coding;
- synthetic VCF SHA-256: `983ee73fe06240765e19283f83986b2a7084ada6b817adce2d1e83bcfdf79698`;
- synthetic index SHA-256: `2902220e924977ad8e5a1324607bcea70efb3259d9855fc67b36d2afbbfaa7b9`.

## Privacy and teardown receipt

- Hugging Face token-file count: 0;
- gated challenge filename matches: 0;
- synthetic completion marker: present;
- VM and auto-delete disk: deleted immediately after the test;
- project SSH metadata: removed;
- unused default network and permissive default firewall rules: deleted;
- post-delete counts: 0 instances, 0 disks, 0 snapshots, 0 custom images, 0 reserved addresses;
- retained no-cost shell: dedicated custom VPC/subnet and IAP-only SSH rule for a later separately approved run.

## Claim ceiling and next falsifier

Ceiling: **C1 public infrastructure smoke**. The test shows that the pinned runtime and databases can load and process a structurally valid synthetic GRCh38 sample. It does not show that Exomiser will recover the real causal pair, outperform a baseline, calibrate EPCR, or produce clinical evidence.

Next falsifier: in the private, non-agent-visible run, the supplied VCF must expose usable sample/genotype/call-quality fields and yield at least one defensible recessive/compound-heterozygous candidate under the frozen baseline. Otherwise escalate to FASTQ only through a new cost/privacy decision.
