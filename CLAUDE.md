# CLAUDE.md — json2csv

Agent guide for the **json2csv** project: a CLI tool that converts JSON files
to CSV format. Stack-agnostic workflow; this file is the single source of
truth for every agent skill operating on this repo.

---

## Project overview

**json2csv** — a command-line tool (Python 3.11+, Click) that reads JSON from
a file or stdin and writes CSV to a file or stdout. Intended for individual
developers and data analysts needing quick JSON→CSV conversion.

Scale: personal / small-team utility. Lifespan: medium-lived, maintained.

---

## Workflow conventions

| Key | Value |
|---|---|
| **Forge** | GitHub (`gh` CLI) |
| **Default branch** | `main` |
| **Branch naming** | `feat/<NN>-<slug>`, `fix/<slug>`, `docs/<slug>` |
| **PR base** | always `main` |
| **Commit style** | conventional commits (`feat:`, `fix:`, `chore:`, `docs:`, `test:`) |
| **Docs language** | English |
| **Verification gate** | `ruff check . && pytest` (both must be green before any commit) |
| **Test runner** | pytest |
| **Linter** | ruff |

**Never work on `main` directly.** One PR per unit of work, always against
`main`. Never stack PRs.

---

## Documentation map

| Doc | Path | Purpose |
|---|---|---|
| This guide | `CLAUDE.md` | Agent instructions, conventions |
| Roadmap | `docs/features/ROADMAP.md` | Feature registry + status |
| SPEC template | `docs/features/_TEMPLATE/SPEC.md` | Feature planning template |
| Fix index | `docs/fix/README.md` | Fix tracker |
| Workflow tutorial | `docs/workflow/README.md` | End-to-end workflow guide |
| Ship decisions | `docs/features/SHIP_DECISIONS.md` | Autopilot run policy |
| Process log | `docs/PROCESS.md` | How the repo reached its current state (demo narrative) |

---

## Architecture

Flat modular layout — proportional to a personal CLI utility:

```
src/json2csv/
  __init__.py      package entry
  converter.py     pure conversion logic (JSON → CSV rows)
  cli.py           Click entry point; wires converter to stdin/stdout/files
tests/
  test_converter.py
  test_cli.py
pyproject.toml     build + ruff + pytest config
```

No layers, no dependency injection, no named architecture pattern. `converter.py`
is pure Python (no Click dependency) so it is trivially testable. `cli.py` is the
thin shell that handles I/O and invokes `converter.py`.

---

## Verification gate

```sh
ruff check . && pytest
```

Both commands must exit 0 before any commit. Never commit red.

---

## Sensitive areas

None declared for this project.

---

## Style & conventions

- Python 3.11+; type hints on all public functions.
- `ruff` for linting and formatting (configured in `pyproject.toml`).
- `pytest` with no mocking of stdlib (json/csv are stable).
- CLI output to stdout; errors to stderr with non-zero exit code.
- README updated whenever a user-facing flag or behaviour changes.
