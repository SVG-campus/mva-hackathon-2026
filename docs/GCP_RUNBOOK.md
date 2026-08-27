# GCP runbook — public preflight complete; conditional private execution

## Decision

Use a **new dedicated GCP project**, not GitHub and not Kaggle, for the private VCF-first run. GitHub is the wrong storage boundary for gated patient data; Kaggle would add a second hosted dataset/notebook platform and an avoidable data-release ambiguity. GCP is explicitly contemplated by the challenge's cloud-compute rule and supports short-lived, auditable deletion.

On 2026-08-25 the user authorized a dedicated project and public-only toolchain preflight under the USD 20 ceiling. The exact project/resource identifiers are retained only in an ignored local state file. No gated challenge data or Hugging Face token entered the VM.

The user has accepted the dataset terms. The organizer's 2026-08-26 point-by-point guidance permits hosted processing when the service takes no rights in the data, performs no training, and uses only limited-purpose, time-bounded retention. Before private execution, complete `docs/PROVIDER_TERMS_CHECKLIST.md` for GCP and any annotation or AI service actually used. Authentication must be interactive; credentials and tokens must never be pasted into chat, source, shell history, or captured logs. Patient-derived content remains unavailable to this agent until the exact Codex/OpenAI plan and settings independently pass the same checklist.

## Frozen first-run envelope

| Resource | Setting |
|---|---|
| Project | brand-new, challenge-only project |
| Region/zone | `us-central1` / `us-central1-a`, unless policy requires another US region |
| VM | `e2-standard-8` (8 vCPU, 32 GB RAM), no GPU |
| Boot disk | 200 GB `pd-balanced`, encrypted by default, auto-delete |
| Lifetime | maximum six hours; instance termination action `DELETE` |
| Identity | OS Login/IAP for SSH; no VM service account and no API scopes |
| Network | dedicated VPC; SSH ingress only from Google's IAP TCP-forwarding range |
| Data scope | VCF, index, phenotype file, public annotation assets; no FASTQ on first run |
| Spend | Console estimate expected under USD 10; never proceed above user-approved USD 20 ceiling |

Google bills a running VM even when idle; after the first minute it is billed by the second. A stopped VM avoids compute charges but persistent disks can continue billing. Therefore the default route deletes the instance and boot disk rather than stopping it. GCP budget alerts are monitoring controls, not spending caps.

## Owner-side preflight

1. Create or select a brand-new project that contains no other workloads.
2. Link the intended billing account and note the exact project ID.
3. In the Pricing Calculator/Console, verify the six-hour estimate for the frozen envelope.
4. Create a USD 20 budget alert at 25%, 50%, 75%, 90%, and 100%, while acknowledging that it does not cap charges.
5. Run `gcloud auth login` only in the user's own interactive terminal. Never share the resulting credential material or create application-default credentials unless a separately reviewed workflow actually requires them.
6. Record explicit approval of the project ID and ceiling before resource creation.

## Proposed creation commands

These are a reviewed template, not commands to run blindly. Replace only the three owner variables. Keep one PowerShell session end-to-end.

```powershell
$mvaProjectId = 'REPLACE_WITH_DEDICATED_PROJECT_ID'
$mvaZone = 'us-central1-a'
$mvaRegion = 'us-central1'
$mvaNetwork = 'mva-private-net'
$mvaSubnet = 'mva-private-subnet'
$mvaVm = 'mva-vcf-preflight'

if ($mvaProjectId -eq 'REPLACE_WITH_DEDICATED_PROJECT_ID') { throw 'Set the dedicated project ID first.' }

gcloud config set project $mvaProjectId
gcloud services enable compute.googleapis.com iap.googleapis.com --project $mvaProjectId

gcloud compute networks create $mvaNetwork `
  --project $mvaProjectId `
  --subnet-mode=custom

gcloud compute networks subnets create $mvaSubnet `
  --project $mvaProjectId `
  --network $mvaNetwork `
  --region $mvaRegion `
  --range 10.42.0.0/24 `
  --enable-private-ip-google-access

gcloud compute firewall-rules create mva-allow-iap-ssh `
  --project $mvaProjectId `
  --network $mvaNetwork `
  --direction INGRESS `
  --action ALLOW `
  --rules tcp:22 `
  --source-ranges 35.235.240.0/20 `
  --target-tags mva-iap

gcloud compute instances create $mvaVm `
  --project $mvaProjectId `
  --zone $mvaZone `
  --machine-type e2-standard-8 `
  --network-interface "network=$mvaNetwork,subnet=$mvaSubnet" `
  --tags mva-iap `
  --no-service-account `
  --no-scopes `
  --image-family ubuntu-2404-lts-amd64 `
  --image-project ubuntu-os-cloud `
  --boot-disk-size 200GB `
  --boot-disk-type pd-balanced `
  --boot-disk-auto-delete `
  --metadata enable-oslogin=TRUE,block-project-ssh-keys=TRUE `
  --shielded-secure-boot `
  --shielded-vtpm `
  --shielded-integrity-monitoring `
  --max-run-duration 21600s `
  --instance-termination-action DELETE `
  --labels purpose=mva-hackathon,retention=ephemeral
```

Before any private data is retrieved, confirm that the VM exists once, has a deletion deadline, has no service account, and has exactly one auto-delete boot disk. Do not echo the Hugging Face token or patient filenames into captured logs.

## Verify deletion after every run

```powershell
gcloud compute instances describe $mvaVm --project $mvaProjectId --zone $mvaZone
gcloud compute disks list --project $mvaProjectId --filter="name=($mvaVm)"
gcloud compute snapshots list --project $mvaProjectId
gcloud compute images list --project $mvaProjectId --no-standard-images
```

Expected after automatic deletion: the instance lookup returns not found; the disk filter returns zero rows; snapshots and custom images are empty. If the VM must be stopped for a resumable debug run, record the disk cost and a deletion timestamp no more than 24 hours later.

## Tear down the no-cost network shell

Only after the instance and disk checks are empty:

```powershell
gcloud compute firewall-rules delete mva-allow-iap-ssh --project $mvaProjectId --quiet
gcloud compute networks subnets delete $mvaSubnet --project $mvaProjectId --region $mvaRegion --quiet
gcloud compute networks delete $mvaNetwork --project $mvaProjectId --quiet
```

At the final post-hackathon deletion gate, the safest disposition is deletion of the dedicated project after the owner verifies it contains no shared resources. Project deletion and billing unlinking are manual owner approvals, not automatic steps in this runbook.

## Primary GCP references

- VM stop/start behavior and residual-resource billing: https://docs.cloud.google.com/compute/docs/instances/stop-start-instance
- Persistent-disk encryption at rest: https://docs.cloud.google.com/compute/docs/disks/disk-encryption
- Budget alerts and their non-capping limitation: https://docs.cloud.google.com/billing/docs/how-to/budgets
- Current disk pricing: https://cloud.google.com/compute/disks-image-pricing
- Current VM pricing and per-second billing after the first minute: https://cloud.google.com/products/compute/pricing

## Falsifiers and stop rules

- Stop before creation if the project is not dedicated, the estimate exceeds the approved ceiling, or deletion controls cannot be verified.
- Stop before data retrieval if shell history, command logging, notebook telemetry, or network egress could expose patient-level content.
- Delete the VM immediately if unexpected snapshots, service-account scopes, public artifacts, or nonessential agents are present.
- Escalate disk/CPU or retrieve FASTQs only through a separate decision packet and owner approval.
