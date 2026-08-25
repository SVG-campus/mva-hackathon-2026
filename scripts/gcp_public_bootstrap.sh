#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y --no-install-recommends \
  bcftools \
  ca-certificates \
  curl \
  git \
  jq \
  openjdk-21-jre-headless \
  tabix \
  unzip \
  wget

install -d -m 0755 /opt/mva-public

{
  printf 'bootstrap_completed_utc='
  date -u +%Y-%m-%dT%H:%M:%SZ
  java -version 2>&1
  tabix --version 2>&1 | head -n 1
  bcftools --version | head -n 1
  git --version
} > /opt/mva-public/bootstrap_receipt.txt

touch /var/lib/mva-public-bootstrap.done
