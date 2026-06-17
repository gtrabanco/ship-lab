# Checklist — 05 human-test-sample

**Gate:** `ruff check . && pytest` — 29/29 ✓ (no Python changes)

| Item | Status |
|---|---|
| Schema migration | n/a |
| Core layer unchanged | ✓ (no `src/` edits) |
| Tests pass | ✓ 29/29 |
| Ruff green | ✓ |
| New deps | n/a (shell script only) |
| Output files gitignored | ✓ `examples/out_*.csv` added to `.gitignore` |
| Script executable bit set | ✓ |
| All three open 👤 items addressed | ✓ (features 03 + 04 human checks covered) |

## Live run verification

```
examples/out_comma.csv  — header: id,name,active,address.city,address.country,tags ✓
examples/out_tab.csv    — header tab-separated (^I confirmed via cat -A) ✓
examples/out_stdin.csv  — identical to out_comma.csv ✓
```

## Decisions not in SPEC

- Script requires `json2csv` on PATH; README instructs `pip install -e .` first.
  Added a note that the venv must be activated (or the package installed globally).
