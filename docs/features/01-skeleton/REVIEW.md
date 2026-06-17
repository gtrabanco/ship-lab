# Review — 01-skeleton

**Branch:** feat/01-skeleton · **Diff vs main:** 8 files, 94 insertions

## Skipped axes
design, accessibility, SEO, brand — no UI surface (Console/CLI project).

## Findings

| Axis | File | Finding | Sev | Class | Route |
|---|---|---|---|---|---|
| tech-debt | `src/json2csv/__init__.py:3` | `__version__` hardcoded — use `importlib.metadata.version()` before any published release | low | postpone | issue + trigger (before first release) |
| code-review | `tests/test_converter.py:5` | `assert __version__ == "0.0.1"` pins exact version; will fail at next bump | low | postpone | fix in version-bump commit |
| security | `ci.yml:6-7` | GHA actions not SHA-pinned | low | intentional-tradeoff | accepted for personal utility scale |
| api-ergonomics | `cli.py:10` | Docstring forward-declares FILE arg not yet present | info | ignore | feature 02 scope |
| spec-drift | — | All 5 AC + both dev scenarios ✓ | — | none | — |

**fix-now: 0** · Gate: ruff PASS, pytest 2/2 PASS.

## Manual verification checklist
- [ ] `pip install -e .` works from a clean clone on macOS and Linux
- [ ] `json2csv --version` prints `0.0.1`
- [ ] GitHub Actions CI goes green on the opened PR
