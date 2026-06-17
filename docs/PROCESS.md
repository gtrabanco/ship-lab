# How this repo was built — agentic-workflow process log

`ship-lab` is a live demo of [agentic-workflow](https://github.com/gtrabanco/agentic-workflow).
This document reconstructs the whole journey from an empty repository to its current state,
mapping **every commit to the skill that produced it** and the artifacts it left behind. It
is the "making of" companion to the [README](../README.md).

> The product being built is **json2csv**, a small Python/Click CLI (JSON → CSV). It is
> deliberately tiny — the interesting thing here is the *process*, not the tool.

---

## Timeline at a glance

| Stage | Commit(s) | Branch | Skill / step | What it produced |
|---|---|---|---|---|
| 0 · Init | `34429e5` | `main` | manual bootstrap | empty lab repo |
| 1 · Founding | `76e85bd` → `a4c37cf` | `docs/ship-founding` | `ship-roadmap` (founding) | CLAUDE.md, roadmap, ship decisions, workflow + fix docs, GitHub templates |
| 2 · Plan 01 | `e4be43b` | `feat/01-skeleton` | `plan-feature` | `01-skeleton/SPEC.md`, roadmap flip → `in-progress` |
| 3 · Execute 01 | `01d33c9` | `feat/01-skeleton` | `execute-phase` | `pyproject.toml`, package scaffold, ruff/pytest config, GitHub Actions CI |
| 4 · Review 01 | `9720676` | `feat/01-skeleton` | `review-change` | review report — 0 fix-now |
| 5 · Merge 01 | `f205c62` (PR #2) | `main` | merge | feature 01 lands on `main` |
| 6 · README reframe | `c69ddb6` → `0d6aa09` (PR #1) | `docs/readme-hook` | `docs` | README reframed as a workflow hook + this process log |
| 7 · Plan 02 | `a0e08ce` | `feat/02-basic-json-to-csv` | `plan-feature` | `02/SPEC.md`, roadmap flip |
| 8 · Execute 02 | `f705178`, `f96668a` | `feat/02-basic-json-to-csv` | `execute-phase` | `converter.py` + `cli.py`, utf-8 encoding fix |
| 9 · Review 02 | `0ceac12`, `5987ed0` | `feat/02-basic-json-to-csv` | `review-change` | 1 fix folded (guard non-object rows, normalize bool/null) |
| 10 · Merge 02 | `170b9f5` (PR #5), `0a65ef0` | `main` | merge + flip | feature 02 lands, roadmap flip → `done` |
| 11 · Fix 01 · issue #4 | `13a4350`, `c1d4a84` → `097609e` (PR #6), `6e3f9dc` | `fix/01-click-exception` | `triage-issue` → `plan-fix` → `execute-phase --fix` | `click.ClickException` error handling |
| 12 · Plan 03 | `ca0261b` | `feat/03-delimiter-flag` | `plan-feature` | `03/SPEC.md`, roadmap flip |
| 13 · Execute 03 | `ddc0ece` | `feat/03-delimiter-flag` | `execute-phase` | `-d`/`--delimiter` flag wired to `convert()` |
| 14 · Review 03 + fold | `b48dff9`, `4103b8d`, `3bffc6e` | `feat/03-delimiter-flag` | `review-change` | loop pass 0 fix-now; standalone pass caught invalid-delimiter traceback → guard folded in |
| 15 · Merge 03 | `4a21c34` (PR #8) | `main` | merge | feature 03 lands |
| 16 · Fix 07 · issue #7 | `c72830a` → `ebe9eb5` (PR #9) | `fix/7-delimiter-metavar` | `triage-issue` → `execute-phase --fix` | `--help` shows `CHAR` (metavar) |
| 17 · Sync | `6b4b60d` | `main` | chore | roadmap flip 03 → `done`, fix index updated |

Current `HEAD` of `main`: `6b4b60d` — features 01–03 and fixes #4/#7 all merged.

> **A note on "PR #1".** Two merge commits carry GitHub's `Merge pull request #1` label:
> the founding (`a4c37cf`, `docs/ship-founding`) and the README reframe (`0d6aa09`,
> `docs/readme-hook`). Only the latter is a real remote PR (`gh pr list` shows #1 =
> readme-hook). The founding was a PR-style **local** merge — the history reads like a PR,
> but you won't find that one on GitHub. The real remote PRs are #1, #2, #5, #6, #8, #9.

---

## Stage 0 — Initialise the lab (`34429e5`)

`chore: init lab repo`. An empty repository with a git remote
(`git@github.com:gtrabanco/ship-lab.git`). Nothing else — the blank canvas the workflow
starts from.

## Stage 1 — Founding (`76e85bd`, branch `docs/ship-founding`)

The [`ship-roadmap`](https://github.com/gtrabanco/agentic-workflow/blob/main/skills/ship-roadmap/SKILL.md)
autopilot begins with a single **founding interview** that asks everything up front, then
writes the project's "way of working" to disk so a crash or a fresh clone can reconstruct
the run without re-asking. For this repo it produced:

- **`CLAUDE.md`** — the agent guide and single source of truth: project overview, workflow
  conventions (GitHub forge, `main` base, conventional commits, branch naming), the
  **verification gate** `ruff check . && pytest`, the architecture sketch, and the style rules.
- **`docs/features/ROADMAP.md`** — the feature registry: four features (01–04) with size,
  dependencies and status.
- **`docs/features/SHIP_DECISIONS.md`** — the durable, auditable run policy: the locked
  interview answers (product, features, stack, quality, workflow), the merge policy
  (`human` — autopilot opens PRs, a human merges), model routing, and a silent-decision log.
- **`docs/workflow/README.md`** and **`docs/fix/README.md`** — the workflow quick-reference
  and the (then empty) fix index.
- **`.github/`** — issue and pull-request templates.
- **`.gitignore`** — Python ignores plus the machine-local `docs/features/.ship-run.log`.

The interview answers that shaped everything (recorded in `SHIP_DECISIONS.md`):

- **Product** — a CLI to convert JSON (file/stdin) to CSV (file/stdout), for developers and
  data analysts; a personal / small-team utility.
- **Features** — must-have 01–03, can-wait 04; out of scope: schema validation, non-JSON
  input, GUI.
- **Stack** — Python 3.11+, Click, flat-modular architecture (`converter.py` pure, `cli.py`
  the I/O shell).
- **Quality & ops** — pytest (happy path + edge cases), GitHub Actions CI (ruff + pytest),
  no secrets, gate `ruff check . && pytest`.
- **Workflow** — English docs, GitHub via `gh`, **human** merge, budget caps.

Merged to `main` at `a4c37cf`, which becomes the baseline every feature branches from.

## Stage 2–5 — Feature 01: skeleton (`feat/01-skeleton`, PR #2)

The first roadmap feature ran the full loop, one skill per stage:

- **Plan** (`e4be43b`) — [`plan-feature`](https://github.com/gtrabanco/agentic-workflow/blob/main/skills/plan-feature/SKILL.md)
  wrote `docs/features/01-skeleton/SPEC.md` (installable package, green `ruff`, green
  `pytest`, a GitHub Actions CI workflow, the stub modules) and flipped the roadmap row to
  `in-progress`. Doc-first: the feature is fully specified before any code exists.
- **Execute** (`01d33c9`) — `execute-phase` scaffolded the package: `pyproject.toml`, the
  `src/json2csv/` modules, ruff + pytest configuration, and the `.github/workflows/` CI that
  runs the gate on 3.11 / 3.12 / 3.13.
- **Review** (`9720676`) — `review-change` produced a classified report: 0 fix-now.
- **Merge** (`f205c62`, PR #2) — the skeleton lands on `main`, satisfying the depends-on
  closure for every later feature.

## Stage 6 — README reframe (`c69ddb6`, branch `docs/readme-hook`, PR #1)

A docs-only PR reframed the `README` from a plain project readme into a **hook for the
agentic-workflow demo** and added the first version of this process log.

## Stage 7–10 — Feature 02: basic JSON → CSV (`feat/02-basic-json-to-csv`, PR #5)

The core conversion feature:

- **Plan** (`a0e08ce`) — SPEC + roadmap flip.
- **Execute** (`f705178`, `f96668a`) — `converter.py` (pure JSON-array → CSV-rows logic) and
  `cli.py` (the Click I/O shell), then a follow-up specifying `utf-8` encoding on
  `click.File`.
- **Review** (`0ceac12`, `5987ed0`) — `review-change` found one fix-now issue and **folded it
  into the branch**: guard against non-object array elements, and normalize `True`/`False`/
  `None` to `true`/`false`/`""` in CSV output.
- **Merge** (`170b9f5`, PR #5; flip `0a65ef0`) — feature 02 lands; roadmap flips to `done`.

## Stage 11 — Fix 01: idiomatic errors (`fix/01-click-exception`, issue #4, PR #6)

A review finding on feature 02 was deferred to **issue #4** rather than inlined. Later
`triage-issue` judged its trigger met (before feature 03), so `plan-fix` →
`execute-phase --fix` replaced ad-hoc `click.echo(err=True) + sys.exit(1)` with idiomatic
`click.ClickException` (clean `Error:` to stderr, exit 1). Merged via PR #6.

## Stage 12–15 — Feature 03: delimiter flag (`feat/03-delimiter-flag`, PR #8)

- **Plan** (`ca0261b`) — SPEC + roadmap flip.
- **Execute** (`ddc0ece`) — the `-d` / `--delimiter` option (default `,`) wired through to
  `convert()`.
- **Review + fold** (`b48dff9`, `4103b8d`, `3bffc6e`) — the in-loop review reported 0
  fix-now, but a **standalone `review-change` second pass** live-probed invalid delimiters and
  found they dumped a raw Python traceback. The branch merged `main` (to sit on PR #6's
  `ClickException` baseline) and folded in a guard rejecting multi-char, empty, and
  quote/newline delimiters with a clean error. Cosmetic `metavar` nit deferred to **issue #7**.
- **Merge** (`4a21c34`, PR #8) — feature 03 lands.

## Stage 16 — Fix 07: delimiter metavar (`fix/7-delimiter-metavar`, issue #7, PR #9)

`triage-issue` → `execute-phase --fix` added `metavar="CHAR"` so `--help` shows
`-d, --delimiter CHAR` instead of the generic `TEXT`. Merged via PR #9.

---

## Current state

**Done:** the project is founded and **features 01–05 and fixes #3/#4/#7/#11 are all merged**,
each through the full plan → execute → review → audit → merge loop.

| # | Feature | Status |
|---|---|---|
| 01 | skeleton (packaging, ruff, pytest, CI) | ✅ done |
| 02 | basic JSON → CSV | ✅ done |
| 03 | `--delimiter` flag | ✅ done |
| 04 | nested-object flatten | ✅ done (PR #12) |
| 05 | human-test sample | ✅ done (PR #14) |
| 06 | array-index expansion | ⏳ planned |
| 07 | release / publish | ⏳ planned |

The CLI is fully functional: `json2csv input.json`, stdin/stdout streaming, `-o/--output`,
`-d/--delimiter` with validation, boolean/null normalization, nested-object flattening to
dot-notation columns, and list-cell JSON encoding. The `__version__` is now read from
installed package metadata (`importlib.metadata`) so version bumps in `pyproject.toml`
propagate automatically.

The verification gate (`ruff check . && pytest`) is green — **32 tests** across
`test_cli.py` and `test_converter.py`.

**Open issues:** none — all previously open issues (#3, #4, #7, #11) are resolved and closed.

**Workflow artifacts:** `.agents/` (vendored agentic-workflow skills) is committed to the
repo. `skills-lock.json` is currently untracked (under triage — see open issue).

---

## What's next

Two features are on the roadmap:

```sh
/plan-feature 06                # array-of-objects → indexed dot-notation columns
/plan-feature 07                # tag v* release + PyPI publish
```

Or run unattended with the autopilot:

```sh
/loop /ship-roadmap --continue
```

The full step-by-step is mirrored in the README's status table and the machine-local
`docs/features/.ship-run.log`.
