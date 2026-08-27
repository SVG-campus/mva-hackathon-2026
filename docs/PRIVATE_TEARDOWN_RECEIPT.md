# Private GCP teardown receipt

- Timestamp: `2026-08-27T13:57:41-07:00`
- Account: owner-selected default GCP account (exact value verified in the private receipt)
- Project: owner-selected default free-credit project (exact value verified in the private receipt)
- Scope: only the exact temporary MVA resources created for this run.

## Deleted resources

- Compute instance: `mva-vcf-private-2026`, zone `us-central1-a`
- Auto-delete boot disk: `mva-vcf-private-2026`, 200 GB `pd-balanced`
- Firewall rule: `mva-allow-iap-ssh-2026`
- Subnetwork: `mva-private-subnet-2026`, region `us-central1`
- Network: `mva-private-net-2026`

## Post-delete verification

Filtered list queries in the selected account/project returned zero matching instances, disks, firewall rules, subnetworks, and networks. No snapshot, image, bucket, service-account credential, or additional hosted processor was created for the private run. Pre-existing unrelated project resources were not modified.

The VM disk deletion is not recoverable. The raw gated files, clinical document copy, phenopacket, genome-scale Exomiser outputs, and private logs formerly stored there were deleted with it. Locally retained artifacts are limited to the organizer-permitted ranked submission, HPO terms, bounded candidate evidence, report/methods files, and non-identifying aggregate receipts.

Claim ceiling: C1 infrastructure/deletion verification. Provider billing data may lag and is not asserted by this receipt.
