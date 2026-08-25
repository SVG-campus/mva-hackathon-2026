# Track 1 scorer mechanics — synthetic verification

Claim ceiling: **C1**. These findings reproduce the public evaluator on synthetic inputs. They do not identify the real causal variants or predict competition placement.

## Exact public mechanics

- The answer key is documented as one clinically validated **compound-heterozygous** pair.
- At most 10 rows are accepted; six live submissions are available per participant.
- A full pair must appear together in a single row to earn full rank credit.
- Rank tiers are 100 points at rank 1, 50 through rank 3, 25 through rank 5, and 10 through rank 10.
- F-max operates on the union of individual variants above each EPCR threshold.
- `finding_type` is informational in the evaluator; the scorer does not exclude `secondary` rows.

## Focused receipt

Command:

```powershell
& 'C:\Users\svillalobosgonzalez1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests -v
```

Result on 2026-08-25: **6 tests passed** in 0.118 seconds.

Verified cases:

1. Exact pair at rank 1 → 100 rank points and F-max 1.0.
2. The same two variants split across rows → only 50 rank points (partial match), even though F-max can still reach 1.0.
3. A high-EPCR false row labeled `secondary` before the true pair → pair moves to rank 2 and F-max falls to 0.8.
4. Exact pair at rank 6 → 10 rank points.
5. More than 10 rows → fail closed.
6. EPCR outside `(0, 1]` → fail closed.

## Material documentation discrepancy

The FAQ/Overview says secondary or incidental findings “won't hurt” the automated score. The public evaluator marks `finding_type` as informational and includes every row in ranking and F-max. Secondary findings are harmless only when their EPCR ordering does not worsen the best threshold or push the causal pair downward.

Decision: keep secondary findings out of the scored CSV unless they are deliberately placed below all primary pairs and have survived a local replay of the exact evaluator. Put broader incidental analysis in the report, not the limited scored rows.

Falsifier: an organizer code update that excludes `finding_type=secondary` from automated scoring. Recheck the Space commit and evaluator hash before every live attempt.
