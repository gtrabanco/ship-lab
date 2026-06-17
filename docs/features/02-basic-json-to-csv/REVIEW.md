# Review — 02-basic-json-to-csv

**Branch:** feat/02-basic-json-to-csv · **Diff vs main:** converter.py, cli.py, tests

## Skipped axes
design, a11y, SEO, brand — no UI surface (Console/CLI project).

## Findings

| Axis | File | Finding | Sev | Class | Route |
|---|---|---|---|---|---|
| code-review | `cli.py:13-15` | `click.File()` without `encoding=` uses locale default — **FIXED** in commit f96668a | low | fix-now → resolved | folded |
| security | `converter.py:24` | CSV injection (formula-prefix values) | low | intentional-tradeoff | accepted; issue #4 |
| code-review | `cli.py:20,25` | `sys.exit(1)` — `raise click.ClickException` more idiomatic | low | postpone | issue #5 |
| tests | `test_cli.py:44` | `test_invalid_json` doesn't assert stderr message | low | postpone | issue #5 |
| code-review | `converter.py:16` | `list[dict]` unparameterized type hint | info | ignore | no runtime impact |
| spec-drift | — | All 7 AC + 7 dev scenarios ✓ | — | none | — |

**fix-now: 0 open** (1 folded). Gate: ruff PASS, pytest 9/9 PASS.

## Manual verification checklist
- [ ] `json2csv input.json` output opens cleanly in a spreadsheet app (Excel/Numbers/Sheets)
- [ ] `json2csv --version` still prints `0.0.1`
- [ ] Non-ASCII (UTF-8) values in JSON round-trip correctly through the CSV
- [ ] GitHub Actions CI green on the PR
