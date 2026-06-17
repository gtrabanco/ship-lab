# SPEC — fix/07 delimiter-metavar

**Issue:** #7 · **Branch:** fix/7-delimiter-metavar · **Status:** in-progress

## Problem

`--help` shows `--delimiter TEXT` (Click's generic default) instead of `--delimiter CHAR`,
so users cannot tell from the help output that a single character is required.

## Fix

Add `metavar="CHAR"` to the `@click.option("-d", "--delimiter", ...)` decorator in
`src/json2csv/cli.py`.

## Acceptance criteria

1. `json2csv --help` shows `--delimiter CHAR` (not `TEXT`).
2. `ruff check . && pytest` exits 0.

## Out of scope

Changing the help text wording; any other option.
