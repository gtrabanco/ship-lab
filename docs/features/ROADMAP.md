# Roadmap

> Status legend: `planned` · `in-progress` · `done`

| # | Slug | Status | Size | Depends on | Summary |
|---|---|---|---|---|---|
| 01 | skeleton | done | S | — | Project scaffold: pyproject.toml, ruff config, pytest setup, GitHub Actions CI (lint + test) |
| 02 | basic-json-to-csv | done | S | 01 | Read flat JSON objects from file/stdin, write CSV rows to file/stdout |
| 03 | delimiter-flag | in-progress | XS | 02 | Add `--delimiter` / `-d` flag (default `,`); pass through to the CSV writer |
| 04 | nested-flatten | planned | S | 02 | Flatten nested JSON objects to dot-notation column names before writing CSV |
