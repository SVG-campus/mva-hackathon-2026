# Track 1 Submission 1 receipt

## Question and authority

Did the owner-approved Model 1 package reach the live Track 1 scorer intact, and what can the returned result support?

The owner explicitly authorized the public GitHub push and Track 1 Attempt 1. No authorization was inferred for another attempt, Track 2, additional cloud spend, or a clinical claim.

## Frozen artifacts

- Participant: `@svillalobos-gonzalez`
- Public repository: https://github.com/SVG-campus/mva-hackathon-2026
- Repository commit submitted: `330427cec27fbb5346e8ada7f55616256e187b9a`
- Predictions file: `svillalobos-gonzalez_model1_bub1b_predictions.csv`
- Predictions SHA-256: `7D2CE57E853EC7EB101C4E396700B6523BDE63AFC96D3F168137A8FE5B6FD412`
- Report file: `svillalobos-gonzalez_model1_report.md`
- Report SHA-256: `B816B529A9444EA5005D5F0508BFEF2545A284FC87D742AAECDA67C85369B7BD`

## Live result

- Recorded submission: Track 1, Submission 1, proband `PROBAND01`
- Submitted: `2026-08-27 21:12 UTC` (`2026-08-27 14:12 PDT`)
- Rank points: **100.0 / 100**
- F-max: **1.000**
- F-max EPCR threshold: **0.46916**
- Scorer message: **Full match at rank 1**
- Live quota after refresh: **1 / 6 attempts used; 5 remain**
- Leaderboard display at verification: **39**, tied at the maximum automated score

The leaderboard number is an ordering among tied perfect-score entries. It is not evidence that this prediction scored below positions 1-38.

## Retained rejected upload

The first upload carried the private VCF sample identifier instead of the challenge's required public identifier `PROBAND01`. The deployed scorer rejected it before recording a submission, and the quota remained 0/6. The validator and generator were repaired, a regression test was added, all 21 tests passed, and the corrected frozen files above were then uploaded. This is retained as a packaging failure, not counted as an attempt or a biological result.

## Interpretation and claim ceiling

The automated result establishes that the submitted two-variant ordering exactly matches the challenge's clinically confirmed hidden answer and puts the full causal pair at rank 1. That is the maximum quantitative Track 1 result.

The result does **not** establish a diagnosis, independent clinical validation, variant phase, medical advice, overall contest victory, or superiority of the method. Innovation, scalability, reproducibility, and report quality are judged separately. The scientific packet therefore retains its **C2 observational challenge-hypothesis ceiling**, including the VUS and unphased-trans limitations, while the narrow scorer-mechanics claim is directly verified.

## Falsifiers, budget, and stop rule

- Falsifier: any later leaderboard refresh showing changed scores, a withdrawn entry, a scorer correction, or modified challenge answer invalidates this receipt's current-live claim.
- Negative control retained: the pre-recording `proband_id` rejection demonstrates that upload success and score recording were not assumed from local validation alone.
- Attempt budget: one authorized Track 1 attempt consumed; five remain. Do not spend another attempt merely to reproduce an already perfect automated score.
- Cost budget: no new cloud resource was created for submission; the private GCP resources remained deleted.
- Stop rule: preserve the remaining attempts until a materially different, prevalidated method or organizer-driven need can improve the separately judged submission package without weakening privacy or reproducibility.
