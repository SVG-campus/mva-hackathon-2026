#!/usr/bin/env bash
set -euo pipefail

readonly private_dir=/srv/mva-private
readonly max_attempts=1800

for ((attempt = 1; attempt <= max_attempts; attempt++)); do
  if [[ -f "${private_dir}/intake_qc.done" ]] && \
      [[ -f /opt/mva-public/exomiser_install.done ]]; then
    break
  fi
  sleep 10
done

if [[ ! -f "${private_dir}/intake_qc.done" ]] || \
    [[ ! -f /opt/mva-public/exomiser_install.done ]]; then
  touch "${private_dir}/orchestrator_wait.timed_out"
  exit 30
fi

if ! sudo bash /tmp/gcp_run_synthetic_exomiser.sh \
    > "${private_dir}/synthetic_driver.log" 2>&1; then
  touch "${private_dir}/synthetic.failed"
  exit 31
fi

if ! /opt/mva-hf/bin/python /tmp/gcp_private_run_exomiser.py \
    > "${private_dir}/exomiser_driver.log" 2>&1; then
  touch "${private_dir}/exomiser.failed"
  exit 32
fi

if ! /opt/mva-hf/bin/python /tmp/gcp_private_result_schema.py \
    > "${private_dir}/schema_driver.log" 2>&1; then
  touch "${private_dir}/schema.failed"
  exit 33
fi

touch "${private_dir}/orchestrator.done"
