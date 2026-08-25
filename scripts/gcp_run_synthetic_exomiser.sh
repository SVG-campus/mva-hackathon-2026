#!/usr/bin/env bash
set -euo pipefail

readonly base_dir=/opt/mva-public
readonly cli_dir="${base_dir}/exomiser-cli-15.1.0"
readonly work_dir="${base_dir}/synthetic-smoke"
readonly results_dir="${work_dir}/results"
readonly plain_vcf="${work_dir}/synthetic-grch38.vcf"
readonly compressed_vcf="${plain_vcf}.gz"
readonly phenopacket="${work_dir}/synthetic-phenopacket.yml"
readonly app_properties="${work_dir}/application-hg38-2602.properties"

test -f "${base_dir}/exomiser_install.done"
install -d -m 0755 "${results_dir}"

cat > "${plain_vcf}" <<'VCF'
##fileformat=VCFv4.2
##source=mva-hackathon-public-synthetic-smoke
##contig=<ID=1,length=248956422,assembly=GRCh38>
##FILTER=<ID=PASS,Description="All filters passed">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype quality">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SYNTHETIC
1	1000000	.	G	A	99	PASS	.	GT:DP:GQ	0/1:50:99
1	1000100	.	A	C	99	PASS	.	GT:DP:GQ	0/1:48:99
VCF

bgzip --force "${plain_vcf}"
tabix --force --preset vcf "${compressed_vcf}"
bcftools view --header-only "${compressed_vcf}" > "${work_dir}/vcf_header.txt"
bcftools query --list-samples "${compressed_vcf}" > "${work_dir}/vcf_samples.txt"

cat > "${phenopacket}" <<'YAML'
---
id: SYNTHETIC
subject:
  id: SYNTHETIC
  sex: MALE
phenotypicFeatures:
  - type:
      id: HP:0000252
      label: Microcephaly
  - type:
      id: HP:0001263
      label: Global developmental delay
htsFiles:
  - uri: synthetic-grch38.vcf.gz
    htsFormat: VCF
    genomeAssembly: hg38
metaData:
  created: '2026-08-25T00:00:00Z'
  createdBy: public-synthetic-smoke
  resources:
    - id: hp
      name: Human Phenotype Ontology
      url: http://purl.obolibrary.org/obo/hp.owl
      version: synthetic-smoke
      namespacePrefix: HP
      iriPrefix: 'http://purl.obolibrary.org/obo/HP_'
  phenopacketSchemaVersion: 1.0
YAML

cat > "${app_properties}" <<PROPERTIES
exomiser.data-directory=${cli_dir}/data
exomiser.hg38.data-version=2602
exomiser.phenotype.data-version=2602
PROPERTIES

export EXOMISER_DATA_DIRECTORY="${cli_dir}/data"
export EXOMISER_HG38_DATA_VERSION=2602
export EXOMISER_PHENOTYPE_DATA_VERSION=2602

cd "${cli_dir}"
start_epoch=$(date +%s)
java -Xmx16g -Dspring.config.location="file:${app_properties}" \
  -jar exomiser-cli-15.1.0.jar analyse \
  --preset exome \
  --sample "${phenopacket}" \
  --vcf "${compressed_vcf}" \
  --assembly hg38 \
  --output-directory "${results_dir}" \
  --output-filename public-synthetic \
  > "${work_dir}/exomiser_stdout.log" 2>&1
end_epoch=$(date +%s)

result_count=$(find "${results_dir}" -maxdepth 1 -type f | wc -l)
test "${result_count}" -gt 0

{
  printf 'synthetic_smoke_completed_utc='
  date -u +%Y-%m-%dT%H:%M:%SZ
  printf 'runtime_seconds=%s\n' "$((end_epoch - start_epoch))"
  printf 'result_file_count=%s\n' "${result_count}"
  printf 'vcf_record_count='
  bcftools view --no-header "${compressed_vcf}" | wc -l
  printf 'sample_count='
  bcftools query --list-samples "${compressed_vcf}" | wc -l
  sha256sum "${compressed_vcf}" "${compressed_vcf}.tbi"
  find "${results_dir}" -maxdepth 1 -type f -printf '%f\n' | sort
} > "${base_dir}/synthetic_smoke_receipt.txt"

touch "${base_dir}/synthetic_smoke.done"
