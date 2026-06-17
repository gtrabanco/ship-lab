# SPEC — 04 nested-flatten

**Size:** S · **Status:** planned · **Branch:** feat/04-nested-flatten

## Goal

Flatten nested JSON objects into dot-notation column names before writing CSV,
so `{"user": {"name": "Ann"}}` becomes a `user.name` column. Lets analysts feed
real-world nested JSON straight into spreadsheets without pre-processing.

## Acceptance criteria

1. A record with a nested object produces dot-notation columns:
   `{"user": {"name": "Ann", "age": 3}}` → header `user.name,user.age`,
   row `Ann,3`.
2. Arbitrary nesting depth flattens fully: `{"a": {"b": {"c": 1}}}` → column
   `a.b.c`.
3. Mixed flat and nested keys in one object both appear: `{"id": 1, "meta":
   {"tag": "x"}}` → `id,meta.tag`.
4. List/array values are written as a single compact JSON-encoded cell, **not**
   index-expanded (e.g. `{"tags": ["a", "b"]}` → column `tags`, value `["a", "b"]`).
5. Mismatched nested shapes across records → union of all leaf columns; missing
   leaves written as empty string (consistent with feature 02).
6. Flat-only input is unchanged — existing CSV output is byte-identical
   (regression guard).
7. Leaf-value normalization still applies: `null` → empty, `true`/`false` →
   `true`/`false` strings.
8. `ruff check . && pytest` exits 0.

## Out of scope

- **Array index expansion** (`tags.0`, `tags.1`) — lists stay as one JSON cell;
  index-flattening is a separate future entry if requested.
- **Configurable separator** — the dot (`.`) is fixed; a `--separator` flag is
  not part of this feature.
- NDJSON input, schema validation, non-JSON formats (out of scope project-wide).

## Silent decisions (resolved from SHIP_DECISIONS.md)

- Flattening lives in `converter.py` (Click-free) as a pure helper applied to
  every record inside `convert()`, so file and stdin paths share it; `cli.py`
  needs no change. Keeps the converter trivially testable (per Architecture).
- Separator is `.` — matches the roadmap summary ("dot-notation") and is the
  conventional flatten separator. No flag (Round 2 scope was must-have 01–03;
  04 is the lone can-wait, kept minimal).
- Lists serialized with `json.dumps(value, ensure_ascii=False)` into one cell —
  lossless and re-parseable, avoids inventing index semantics this feature does
  not own (AC4).
- Empty nested object `{}` contributes no leaf columns (it has no leaves);
  documented edge case, asserted in tests.
- Key ordering: leaves emitted in depth-first insertion order, preserving the
  feature-02 "first occurrence wins" union rule across records.

## Dev scenarios (tests-first)

- `test_flatten_single_level` — one nested object → `parent.child` columns (AC1).
- `test_flatten_deep` — 3-level nesting → `a.b.c` (AC2).
- `test_flatten_mixed_flat_and_nested` — flat + nested keys coexist (AC3).
- `test_flatten_list_as_json_cell` — list value → single JSON-encoded cell (AC4).
- `test_flatten_mismatched_shapes` — records with differing nested keys → union
  header, empty for missing leaves (AC5).
- `test_flat_only_unchanged` — flat input output is byte-identical to pre-feature
  behaviour (AC6 regression).
- `test_flatten_leaf_normalization` — nested `null`/`true`/`false` leaves
  normalize correctly (AC7).
- `test_flatten_empty_nested_object` — `{"a": {}}` → no `a*` columns (edge case).
- `test_cli_nested_end_to_end` — CLI invocation with nested JSON file produces
  flattened CSV (one integration check in `test_cli.py`).

## Deploy & rollback

n/a — additive, pure code change; no migration, data, or config impact.
Rollback is reverting the PR.
