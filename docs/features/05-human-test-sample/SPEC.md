# SPEC — 05 human-test-sample

**Size:** S · **Status:** planned · **Branch:** feat/05-human-test-sample

## Goal

Provide a ready-to-run sample so any human can quickly verify the behaviours that
automated tests cannot confirm: column alignment in a spreadsheet, tab-delimited
rendering, and JSON-encoded list cells. Closes all open 👤 human-test items from
features 03 and 04 in one self-contained step.

## Acceptance criteria

1. `examples/input.json` exists: a JSON array of 5–7 objects with flat fields,
   at least one nested object (2 levels deep), at least one list-valued field,
   and at least one `null`/`true`/`false` leaf — covering every normalisation and
   flattening rule exercised by the automated tests.
2. `examples/run_sample.sh` is executable and runs three scenarios in sequence:
   - **comma CSV** — default output written to `examples/out_comma.csv`
   - **tab CSV** — `-d $'\t'` output written to `examples/out_tab.csv`
   - **stdin pipe** — pipes `input.json` through `json2csv` to `examples/out_stdin.csv`
   Each scenario prints a one-line label before running so the human can follow along.
3. `examples/out_*.csv` are excluded from git via `.gitignore`, so every user
   generates their own outputs locally.
4. The README gains a **"Try the sample"** section (after the feature table)
   explaining: install the package, run the script, and what to look for in each
   output file — one bullet per human check.
5. All three human-test items previously open across features 03 and 04 are
   addressed by the sample:
   - 👤 Tab-delimited output opens cleanly in a spreadsheet app (feature 03)
   - 👤 Flattened CSV (`user.name`-style headers) aligns correctly in a spreadsheet (feature 04)
   - 👤 JSON-encoded list cell (`"[…]"`) displays / re-imports acceptably (feature 04)
6. `ruff check . && pytest` exits 0 (no regressions — the sample is data + shell,
   no Python changes).

## Out of scope

- Automated spreadsheet-open testing — the whole point is human eyes.
- Multiple sample files for different schemas.
- A `Makefile` target or `pytest` fixture for the sample (keep it a plain shell script).
- Any change to `src/` or `tests/`.

## Silent decisions (resolved from SHIP_DECISIONS.md)

- **Domain for the sample data:** a small employee/team roster — relatable, obviously
  fake, no PII concerns, exercises all field types naturally.
- **5 records:** enough to show union-header behaviour (mismatched keys across rows)
  without being noisy.
- **Script uses `#!/usr/bin/env bash` and `set -e`** — portable, fails fast on error.
- **Script assumes the package is installed** (`pip install -e .` or equivalent);
  it does not set up a venv — that's the user's responsibility, documented in the
  README section.
- **`.gitignore` pattern `examples/out_*.csv`** — scoped to generated outputs;
  `examples/input.json` and `examples/run_sample.sh` are tracked.

## Sample JSON design

```json
[
  {
    "id": 1, "name": "Alice Nguyen", "active": true,
    "address": {"city": "Madrid", "country": "ES"},
    "tags": ["python", "data"]
  },
  {
    "id": 2, "name": "Bob Chen", "active": false,
    "address": {"city": "Barcelona", "country": "ES"},
    "tags": ["figma", "css", "ux"]
  },
  {
    "id": 3, "name": "Carol Smith", "active": true,
    "address": {"city": "Lisbon", "country": "PT"},
    "tags": ["go", "infra"]
  },
  {
    "id": 4, "name": "David Park", "active": true,
    "address": {"city": "Berlin", "country": "DE"},
    "tags": []
  },
  {
    "id": 5, "name": "Eva Rossi", "active": null,
    "address": {"city": "Rome", "country": "IT"},
    "tags": ["ml", "python", "data"]
  }
]
```

Fields exercised: flat int (`id`), flat string (`name`), boolean (`active` → `true`/`false`),
`null` (`active` on record 5 → empty), nested object 1-level (`address.city`,
`address.country`), list (compact JSON cell), empty list (record 4 → `[]`).

## Dev scenarios (tests-first)

No new automated tests — the only new runnable artefact is a shell script.
Gate check (`ruff check . && pytest`) confirms no regressions.

- **Manual run:** `bash examples/run_sample.sh` from the repo root produces
  `examples/out_comma.csv`, `examples/out_tab.csv`, `examples/out_stdin.csv`.
- **Human checks (see README section):**
  - Open `out_tab.csv` in a spreadsheet — columns must align, no merged cells.
  - Open `out_comma.csv` — `address.city` and `address.country` appear as separate
    columns; `tags` column contains a JSON-encoded string.
  - Re-import `tags` cell value: it must parse as valid JSON (`json.loads`).

## Deploy & rollback

n/a — additive: new data file, new shell script, `.gitignore` line, README section.
No migration, no config change. Rollback: revert the PR.
