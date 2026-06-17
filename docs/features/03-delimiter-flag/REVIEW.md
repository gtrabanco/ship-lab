# Review — 03 delimiter-flag

**Date:** 2026-06-17 · **Branch:** feat/03-delimiter-flag vs main

## Scope

`src/json2csv/cli.py`, `src/json2csv/converter.py`, `tests/test_cli.py`,
`tests/test_converter.py`, `docs/features/03-delimiter-flag/SPEC.md`.

Skipped: design, a11y, SEO, brand — Console/CLI project, no UI surface.

## Findings

| Axis | Finding | Sev | Class | WHY | Route |
|---|---|---|---|---|---|
| api-ergonomics | `--delimiter` help shows `TEXT` not `CHAR` | low | postpone | Cosmetic; out of scope per SPEC | issue #7, trigger: first user confusion or pre-1.0 polish |
| verify / bug | Invalid delimiter (multi-char, empty, quote/newline) dumped a Python traceback instead of a clean error | low→med | **fixed** | Contradicted the clean-error convention from issue #4; first-pass review flagged it for manual check but never executed it | folded into PR #8 (guard in `cli.py` + 3 tests) |

**0 open fix-now findings after the fold.**

## Second pass — standalone review-change (2026-06-17, after PR #6 merged)

Live edge-case probing of the delimiter flag surfaced the traceback finding
above. The first-pass review (in the ship-roadmap loop) only listed it as a
manual-verification item and never ran it. Probed values and pre-fix behaviour:

- `-d "||"` (multi-char) → `TypeError` traceback
- `-d ""` (empty) → `TypeError` traceback
- `-d '"'` (quote char) → `ValueError` traceback
- value containing the delimiter → correctly quoted (no issue)

Fix folded into the branch:
- `cli.py`: guard rejecting `len != 1` and the quote/`\r`/`\n` chars with a
  `ClickException` — clean `Error:` message, exit 1, no traceback.
- Tests: `test_delimiter_multichar_rejected`, `test_delimiter_empty_rejected`,
  `test_delimiter_quote_rejected`.
- Merged `main` into the branch first so the guard sits on PR #6's
  `ClickException` baseline; verified the merged result passes the gate (20/20).

## SPEC drift

None after the fold. AC7 (invalid delimiter → clean error) added to the SPEC to
record the reconciled decision; all 8 ACs satisfied and mapped to tests.

## Live execution

- Tab-delimited: ✓ `a\tb` / `hello world\ttwo`
- Semicolon-delimited: ✓ `a;b` / `1;2`
- Default comma: ✓ unchanged
- `--help` shows `--delimiter` with `[default: ,]`: ✓
- Invalid delimiters (`||`, ``, `"`): ✓ clean `Error:` message, exit 1
- Gate: 20/20 green

## Manual-verification checklist

- [x] 👤 Tab-delimited output opens cleanly in a spreadsheet app _(human visual check)_
