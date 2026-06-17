# Review — 03 delimiter-flag

**Date:** 2026-06-17 · **Branch:** feat/03-delimiter-flag vs main

## Scope

`src/json2csv/cli.py`, `src/json2csv/converter.py`, `tests/test_cli.py`,
`tests/test_converter.py`, `docs/features/03-delimiter-flag/SPEC.md`.

Skipped: design, a11y, SEO, brand — Console/CLI project, no UI surface.

## Findings

| Axis | Finding | Sev | Class | WHY | Route |
|---|---|---|---|---|---|
| api-ergonomics | `--delimiter` help shows `TEXT` not `CHAR` | low | postpone | Cosmetic; csv raises naturally on multi-char; out of scope per SPEC | issue #7, trigger: first user confusion or pre-1.0 polish |

**0 fix-now findings.**

## SPEC drift

None. All 7 ACs satisfied and mapped to tests.

## Live execution

- Tab-delimited: ✓ `a\tb` / `hello world\ttwo`
- Semicolon-delimited: ✓ `a;b` / `1;2`
- Default comma: ✓ unchanged
- `--help` shows `--delimiter` with `[default: ,]`: ✓
- Gate: 17/17 green

## Manual-verification checklist

- [ ] 👤 Tab-delimited output opens cleanly in a spreadsheet app _(human visual check)_
- [ ] 👤 Multi-char delimiter (e.g. `--delimiter ",,"`) produces a clear error, not silent corruption _(human check)_
