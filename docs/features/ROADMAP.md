# Roadmap

> Status legend: `planned` · `in-progress` · `done`

| # | Slug | Status | Size | Depends on | Summary |
|---|---|---|---|---|---|
| 01 | skeleton | done | S | — | Project scaffold: pyproject.toml, ruff config, pytest setup, GitHub Actions CI (lint + test) |
| 02 | basic-json-to-csv | done | S | 01 | Read flat JSON objects from file/stdin, write CSV rows to file/stdout |
| 03 | delimiter-flag | done | XS | 02 | Add `--delimiter` / `-d` flag (default `,`); pass through to the CSV writer |
| 04 | nested-flatten | done | S | 02 | Flatten nested JSON objects to dot-notation column names before writing CSV |
| 05 | human-test-sample | done | S | 04 | Sample JSON + run script to let humans verify tab-delimited, nested, and list-cell outputs |
| 06 | array-index-expansion | planned | M | 04 | Expand arrays-of-objects to indexed dot-notation columns (e.g. items.0.x, items.1.x) |
| 07 | release-publish | planned | S | — | Tag v* release, publish to PyPI; closes the importlib.metadata loop from fix #3 |
