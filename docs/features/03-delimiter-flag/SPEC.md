# SPEC — 03 delimiter-flag

**Size:** XS · **Status:** in-progress · **Branch:** feat/03-delimiter-flag

## Goal

Add a `--delimiter` / `-d` CLI flag (default `,`) that lets users produce
TSV or any other single-character-delimited output without post-processing.

## Acceptance criteria

1. `json2csv input.json` still produces comma-delimited output (default unchanged).
2. `json2csv -d $'\t' input.json` produces tab-delimited output.
3. `json2csv --delimiter ';' input.json` produces semicolon-delimited output.
4. `-d` / `--delimiter` are aliases for the same flag.
5. The delimiter is passed through to `csv.DictWriter`; no other behaviour changes.
6. `json2csv --help` documents the flag with its default value.
7. An invalid delimiter (multi-character, empty, or a quote/newline character)
   exits non-zero with a clean error message — not a traceback.
8. `ruff check . && pytest` exits 0.

## Out of scope

Multi-character delimiters (rejected, not supported), quote-character control,
nested-object flattening (feature 04), escape-character control.

## Silent decisions (resolved from SHIP_DECISIONS.md)

- The delimiter flag is wired in `cli.py` and forwarded to `convert()`; the
  converter signature gains a `delimiter: str = ","` parameter — keeps
  converter testable without Click.
- Invalid delimiters are validated in `cli.py` and rejected with a clean
  `ClickException` (consistent with the error-handling convention from
  issue #4). `csv` rejects length≠1, the quote char `"`, and `\r`/`\n`; the
  guard pre-empts all of these so the user never sees a raw traceback.
  _(Revised after a standalone `review-change` showed the original
  "raises naturally / out of scope" stance produced a traceback, not a clean
  error.)_

## Dev scenarios (tests-first)

- `test_default_delimiter` — no flag → header and rows comma-separated (regression).
- `test_tab_delimiter` — `-d $'\t'` → tab-separated output.
- `test_semicolon_delimiter` — `--delimiter ';'` → semicolon-separated output.
- `test_delimiter_help` — `--help` output contains `--delimiter`.
- `test_delimiter_multichar_rejected` / `test_delimiter_empty_rejected` /
  `test_delimiter_quote_rejected` — invalid delimiters → clean error, exit 1.

## Deploy & rollback

n/a — additive flag; no migration, no data, no config change.
