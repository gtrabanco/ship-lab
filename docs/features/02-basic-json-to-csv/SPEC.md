# SPEC — 02 basic-json-to-csv

**Size:** S · **Status:** in-progress · **Branch:** feat/02-basic-json-to-csv

## Goal

Read a JSON array of flat objects from a file or stdin; write CSV rows
(header + data) to a file or stdout.

## Acceptance criteria

1. `json2csv input.json` reads `input.json` and writes CSV to stdout.
2. `json2csv < input.json` (stdin) produces identical output.
3. `json2csv input.json -o output.csv` writes CSV to `output.csv` instead of stdout.
4. An empty JSON array (`[]`) produces an empty file (no header, no rows, exit 0).
5. Objects with mismatched keys: union of all keys used as header; missing values
   written as empty string.
6. Non-JSON input exits with a non-zero code and an error message to stderr.
7. `ruff check . && pytest` exits 0.

## Out of scope

Custom delimiter (feature 03), nested-object flattening (feature 04), NDJSON
input, schema validation, non-JSON formats.

## Silent decisions (resolved from SHIP_DECISIONS.md)

- Input format: JSON array of objects `[{…}, …]`. NDJSON deferred (no mention
  in interview).
- Key ordering: preserves insertion order of the first object, then appends
  any new keys seen in subsequent objects (Python 3.7+ dict ordering guarantee).
- Output encoding: UTF-8.
- `-o` / `--output` flag added to `cli.py`; `converter.py` remains Click-free.

## Dev scenarios (tests-first)

- `test_flat_objects` — array of 2 objects, same keys → correct header + rows.
- `test_empty_array` — `[]` → empty output, exit 0.
- `test_mismatched_keys` — objects with different key sets → union header,
  empty strings for missing values.
- `test_invalid_json` — non-JSON input → non-zero exit, stderr message.
- `test_cli_file_arg` — invoke CLI with a temp file, check CSV output.
- `test_cli_stdin` — invoke CLI with stdin piped, check CSV output.
- `test_cli_output_flag` — invoke CLI with `-o`, check file written.

## Deploy & rollback

n/a — no migration, no data, no config change.
