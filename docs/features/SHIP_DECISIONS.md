# Ship Decisions — json2csv autopilot run

This file is the durable, auditable run policy. It is committed and lives on
the default branch. A crash, another machine, or a fresh clone can reconstruct
the full run policy without re-interviewing.

---

## Run mode

| Key | Value |
|---|---|
| **Mode** | `--continue` (human-merge default) |
| **Merge policy** | `human` — the autopilot opens PRs; the human merges |
| **First feature PR** | human-merge required (calibration gate, even in fullauto) |
| **Fullauto** | disabled — `merge: human` |

---

## Interview answers (locked)

### Round 1 — Product
- **What:** CLI tool to convert JSON files/stdin to CSV files/stdout
- **For whom:** individual developers and data analysts
- **Scale ceiling:** personal / small-team utility
- **Lifespan:** medium-lived, maintained utility

### Round 2 — Features
- **Must-have:** 01 skeleton, 02 basic-json-to-csv, 03 delimiter-flag
- **Can-wait:** 04 nested-flatten
- **Out of scope:** JSON schema validation, non-JSON input formats, GUI
- **Ordering:** see ROADMAP.md (dependency chain 01→02→03, 02→04)

### Round 3 — Stack & architecture
- **Language:** Python 3.11+
- **CLI framework:** Click
- **Architecture:** flat modular — `src/json2csv/{converter.py,cli.py}` — proportional to a personal utility; no layers, no named pattern
- **Platform:** macOS / Linux

### Round 4 — Quality & ops
- **Test depth:** workflow (pytest — happy path + key edge cases per feature)
- **a11y / SEO / i18n / perf budgets:** not applicable (CLI)
- **CI:** GitHub Actions — ruff + pytest on every push/PR
- **Secrets posture:** none
- **Verification gate:** `ruff check . && pytest`

### Round 5 — Workflow & autonomy
- **Docs language:** English
- **Forge:** GitHub (`gh` CLI) — verified authenticated ✅
- **Merge policy:** human
- **Sensitive-area list:** none declared
- **Budget caps:** max 16 iterations (4× feature count), 2 retries per red gate, 2 review-fix cycles, 2 audit-fix cycles

---

## Skills directory

Discovered at founding: `~/.agents/skills/` (global install) with Claude Code
symlinks at `~/.claude/skills/`. Subagent prompts reference the execute-phase
skill at `~/.agents/skills/execute-phase/SKILL.md`.

---

## Model routing

| Stage | Tier |
|---|---|
| Planning, review, audit (conductor in-turn) | opus / high |
| Phase execution subagents | sonnet (explicit override) |
| product-audit | hand-off only (fable/max exceeds conductor) |

---

## Silent-decision log

Decisions made without asking (mid-run gaps resolved from this record):
- `2026-06-12` — Founded on `docs/ship-founding` branch (existing repo history present); PR required before loop can start.
- `2026-06-12` — Feature 01 skeleton sized S; all other features' depends-on closure includes 01 (verified in ROADMAP.md).
- `2026-06-12` — pyproject.toml chosen over setup.py (modern Python packaging standard; no library veto in interview).
