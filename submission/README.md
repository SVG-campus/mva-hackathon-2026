# Submission staging

Nothing in this directory is currently approved for a live challenge submission.

- `synthetic/` contains structurally valid but completely artificial fixtures. **Never upload these files to the challenge**; doing so would waste a live attempt.
- `track1_report_scaffold.md` is public-safe methodology text with explicit placeholders. It is not a completed report and contains no candidate result.
- `final/` is gitignored. A final CSV/report may enter that directory only after the private candidate run, evidence review, pinned-evaluator replay, and manual privacy scan.

Before a live Track 1 submission:

```powershell
python scripts\validate_track1_submission.py submission\final\<predictions-file>.csv
```

The user must approve the final files and submission purpose before the irreversible **Submit & Score** click.
