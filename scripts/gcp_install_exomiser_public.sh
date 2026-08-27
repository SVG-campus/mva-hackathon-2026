#!/usr/bin/env bash
set -euo pipefail

readonly base_dir=/opt/mva-public
readonly download_dir="${base_dir}/downloads"
readonly release_version=15.1.0
readonly data_version=2602
readonly cli_archive="exomiser-cli-${release_version}-distribution.zip"
readonly cli_sha256="47faa54d4791686c9dc3f896762834630e9eaf607ad3cf3399074353c3dda248"
readonly cli_size=170449958
readonly hg38_archive="${data_version}_hg38.zip"
readonly hg38_size=23576028714
readonly phenotype_archive="${data_version}_phenotype.zip"
readonly phenotype_size=13478530504
readonly cli_url="https://github.com/exomiser/Exomiser/releases/download/${release_version}/${cli_archive}"
readonly hg38_url="https://g-879a9f.f5dc97.75bc.dn.glob.us/data/${hg38_archive}"
readonly phenotype_url="https://g-879a9f.f5dc97.75bc.dn.glob.us/data/${phenotype_archive}"

install -d -m 0755 "${download_dir}"
cd "${download_dir}"

printf 'download_start_utc=' >> "${base_dir}/exomiser_install.log"
date -u +%Y-%m-%dT%H:%M:%SZ >> "${base_dir}/exomiser_install.log"

download_if_needed() {
  local url=$1
  local archive=$2
  local expected_size=$3
  local actual_size=0

  if [[ -f "${archive}" ]]; then
    actual_size=$(stat -c %s "${archive}")
  fi
  if [[ "${actual_size}" == "${expected_size}" ]]; then
    printf 'reuse_complete_archive=%s bytes=%s\n' "${archive}" "${actual_size}" \
      >> "${base_dir}/exomiser_install.log"
    return 0
  fi
  if (( actual_size > expected_size )); then
    printf 'oversized archive %s: expected %s, found %s\n' \
      "${archive}" "${expected_size}" "${actual_size}" >&2
    return 1
  fi
  curl -fL --retry 5 --retry-delay 5 --continue-at - \
    --output "${archive}" "${url}"
  test "$(stat -c %s "${archive}")" = "${expected_size}"
}

download_if_needed "${cli_url}" "${cli_archive}" "${cli_size}" &
cli_pid=$!
download_if_needed "${hg38_url}" "${hg38_archive}" "${hg38_size}" &
hg38_pid=$!
download_if_needed "${phenotype_url}" "${phenotype_archive}" "${phenotype_size}" &
phenotype_pid=$!

wait "${cli_pid}"
wait "${hg38_pid}"
wait "${phenotype_pid}"

sha256sum "${cli_archive}" "${hg38_archive}" "${phenotype_archive}" \
  > "${base_dir}/exomiser_archives.sha256"
printf '%s  %s\n' "${cli_sha256}" "${cli_archive}" | sha256sum --check --strict

unzip -q "${cli_archive}" -d "${base_dir}"
readonly cli_dir="${base_dir}/exomiser-cli-${release_version}"
test -d "${cli_dir}"
install -d -m 0755 "${cli_dir}/data"

unzip -q "${hg38_archive}" -d "${cli_dir}/data"
rm -f "${hg38_archive}"
unzip -q "${phenotype_archive}" -d "${cli_dir}/data"
rm -f "${phenotype_archive}"
rm -f "${cli_archive}"
chmod -R a+rX "${cli_dir}"

{
  printf 'install_completed_utc='
  date -u +%Y-%m-%dT%H:%M:%SZ
  printf 'exomiser_version=%s\n' "${release_version}"
  printf 'data_version=%s\n' "${data_version}"
  du -sh "${cli_dir}" "${cli_dir}/data"
  df -h /
} >> "${base_dir}/exomiser_install.log"

touch "${base_dir}/exomiser_install.done"
