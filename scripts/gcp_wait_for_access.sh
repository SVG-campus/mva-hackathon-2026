#!/usr/bin/env bash
set -euo pipefail

readonly private_dir=/srv/mva-private
readonly python_bin=/opt/mva-hf/bin/python
readonly max_attempts=1200

install -d -m 0700 "${private_dir}"

for ((attempt = 1; attempt <= max_attempts; attempt++)); do
  if cd /tmp && "${python_bin}" gcp_hf_access_check.py \
      > "${private_dir}/hf_access_safe.json" 2>&1; then
    if ! "${python_bin}" /tmp/gcp_private_intake.py \
        > "${private_dir}/intake_driver.log" 2>&1; then
      touch "${private_dir}/intake.failed"
      exit 21
    fi
    if ! "${python_bin}" /tmp/gcp_private_qc.py \
        > "${private_dir}/qc_driver.log" 2>&1; then
      touch "${private_dir}/qc.failed"
      exit 22
    fi
    touch "${private_dir}/intake_qc.done"
    exit 0
  fi
  sleep 15
done

touch "${private_dir}/access_wait.timed_out"
exit 20
