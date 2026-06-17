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
7. `ruff check . && pytest` exits 0.

## Out of scope

Multi-character delimiters, quote-character control, nested-object flattening
(feature 04), escape-character control.

## Silent decisions (resolved from SHIP_DECISIONS.md)

- The delimiter flag is wired in `cli.py` and forwarded to `convert()`; the
  converter signature gains a `delimiter: str = ","` parameter — keeps
  converter testable without Click.
- No validation of delimiter length; `csv.writer` raises `TypeError` for
  multi-char delimiters naturally (acceptable; out of scope).

## Dev scenarios (tests-first)

- `test_default_delimiter` — no flag → header and rows comma-separated (regression).
- `test_tab_delimiter` — `-d $'\t'` → tab-separated output.
- `test_semicolon_delimiter` — `--delimiter ';'` → semicolon-separated output.
- `test_delimiter_help` — `--help` output contains `--delimiter`.

## Deploy & rollback

n/a — additive flag; no migration, no data, no config change.
