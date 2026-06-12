# SPEC — 01 skeleton

**Size:** S · **Status:** in-progress · **Branch:** feat/01-skeleton

## Goal

Bootstrap the json2csv project: installable Python package, ruff linting,
pytest, and GitHub Actions CI (lint + test on every push/PR).

## Acceptance criteria

1. `pip install -e .` succeeds from the repo root.
2. `ruff check .` exits 0 on a clean tree.
3. `pytest` finds and passes at least a trivial smoke test.
4. A GitHub Actions workflow triggers on push and PR; it runs `ruff check .`
   and `pytest` and must both be green.
5. `src/json2csv/__init__.py`, `converter.py`, and `cli.py` exist (stubs are
   fine — the next feature implements them).

## Out of scope

Actual conversion logic (feature 02), CLI flags (features 03–04).

## Dev scenarios (test list for tests-first)

- `test_package_importable` — `from json2csv import __version__` does not raise.
- `test_cli_help` — `json2csv --help` exits 0 and prints usage.

## Deploy & rollback

n/a — no migration, no data, no config change. Merging the PR is sufficient.
