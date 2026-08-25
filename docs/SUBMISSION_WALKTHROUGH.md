# Submission walkthrough and calendar

Challenge close: **2026-10-24 23:59 UTC**, which is **2026-10-24 16:59 PDT**. Our internal deadline is 48 hours earlier.

## Phase 0 — now through 2026-08-28

- Confirm every team member is 18+ and individually registered.
- Follow the existing hosted-AI/data-handling discussion.
- Post the scorer discrepancy and derived-data questions if the organizers have not already answered them.
- Authorize a dedicated GCP project and a USD 20 maximum only if proceeding with the proposed runbook.
- Do not retrieve gated data through an agent or paste it into a chat.

Exit receipt: registrations checked, written data boundary accepted, source commit rechecked, and cloud authorization recorded.

## Phase 1 — VCF-only preflight, 2026-08-29 through 2026-09-04

- User accepts the dataset terms and authenticates interactively.
- Create the isolated six-hour VM only after the Console estimate is within the approved ceiling.
- Retrieve only the VCF, index, and clinical phenotype file inside the private environment.
- Record hashes, file sizes, VCF headers, sample count, reference build, and tool versions without exporting patient values.
- Run structural QC and the VCF-sufficiency gate.
- Let the VM and disk auto-delete; verify deletion.

Exit receipt: `PASS_VCF_ROUTE`, `ESCALATE_FASTQ`, or `ABSTAIN_DATA_GOVERNANCE`.

## Phase 2 — frozen baseline and challenger, 2026-09-05 through 2026-09-18

- Build the transparent baseline and pre-registered challenger.
- Run phenotype-shuffle, frequency-only, panel-ablation, and pair-format controls.
- Perform manual primary-source review of every candidate in the top 10.
- Keep real coordinates and alleles out of the public repository and hosted tools.

Exit receipt: fixed candidate universe, fixed weights, fixed EPCR mapping, candidate evidence cards, and failed-control log.

## Phase 3 — Track 1 packet and optional Track 2 gate, 2026-09-19 through 2026-10-02

- Produce the ranked CSV with at most 10 rows and each proposed compound-heterozygous pair together in one row.
- Replay the exact pinned evaluator locally.
- Draft the methods form, public report, reproducible synthetic example, environment lockfile, and public-repository privacy audit.
- Evaluate Track 2 only for the leading causal mechanism. Stop if evidence direction, approved status, pediatric exposure, or safety remains indeterminate.

Exit receipt: Track 1 submission candidate frozen; Track 2 `GO` or `NO-GO` recorded.

## Phase 4 — dry run, 2026-10-03 through 2026-10-12

- Recheck the Space commit, rules, evaluator hash, leaderboard, and organizer answers.
- Create the public GitHub repository only after the privacy scan passes.
- Validate links in an incognito/logged-out browser.
- Use the first live Track 1 attempt only with the user's explicit approval.
- Diagnose the result without changing more than one pre-registered factor per subsequent attempt.

Exit receipt: public repository reachable, report downloadable, form complete, score recorded, remaining-attempt count reconciled.

## Phase 5 — final submission, 2026-10-13 through internal close on 2026-10-22

- Freeze code, dependencies, source hashes, report, methods form, and final CSV.
- Complete the Track 2 three-minute public video only if Track 2 passed its gate.
- User performs the irreversible submission clicks while we verify each visible field and attachment.
- Save timestamped confirmation screenshots/receipts that contain no gated patient information.
- Do not spend the final reserve attempt merely because it exists.

## Manual Track 1 checklist

- Ranked CSV, maximum 10 rows, GRCh38, exact required headers.
- `epcr` in `(0, 1]`, monotonically aligned with intended rank.
- Public GitHub URL works without authentication.
- PDF or Markdown report is final and contains no restricted patient-derived material.
- Methods workbook is complete.
- Team and participant information match registration.
- Remaining attempts checked before clicking Submit.

## Manual Track 2 checklist

- One approved existing medication or an explicit abstention.
- Variant-to-gene-to-mechanism-to-drug chain is sourced and directionally consistent.
- Pediatric formulation/exposure, contraindications, tumour-risk implications, and uncertainty are explicit.
- Public GitHub and final report work without authentication.
- Three-minute YouTube/Vimeo link is public and playable.
- Methods workbook is complete.
- The user confirms the single irreversible attempt before clicking Submit.

## Post-close deletion

By 30 days after challenge close, enumerate and delete every source, intermediate, and covered derived dataset from local disks, cloud disks, notebooks, caches, snapshots, trash, and private repositories. Verify absence, retain a non-identifying deletion receipt, and have the user send the organizer-required confirmation email manually.
