# How this repo was built — agentic-workflow process log

`ship-lab` is a live demo of [agentic-workflow](https://github.com/gtrabanco/agentic-workflow).
This document reconstructs the whole journey from an empty repository to its current state,
mapping **every commit to the skill that produced it** and the artifacts it left behind. It
is the "making of" companion to the [README](../README.md).

> The product being built is **json2csv**, a small Python/Click CLI (JSON → CSV). It is
> deliberately tiny — the interesting thing here is the *process*, not the tool.

---

## Timeline at a glance

| Stage | Commit | Branch | Skill / step | What it produced |
|---|---|---|---|---|
| 0 · Init | `34429e5` | `main` | manual bootstrap | empty lab repo |
| 1 · Founding | `76e85bd` | `docs/ship-founding` | `ship-roadmap` (founding) | CLAUDE.md, roadmap, ship decisions, workflow + fix docs, GitHub templates |
| 2 · Merge founding | `a4c37cf` | `main` | PR-style merge | founding lands on `main` |
| 3 · Plan feature 01 | `e4be43b` | `feat/01-skeleton` | `plan-feature` → `plan-feature-scaffold` | `docs/features/01-skeleton/SPEC.md`, roadmap row flipped to `in-progress` |

Current `HEAD`: `feat/01-skeleton` @ `e4be43b` — one commit ahead of `main`, pushed,
**no PR opened yet**.

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
  and the (empty) fix index.
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

## Stage 2 — Founding merged to `main` (`a4c37cf`)

`Merge pull request #1 from gtrabanco/docs/ship-founding`. The founding branch lands on
`main`, which becomes the baseline every feature branches from.

> **Note on "PR #1".** The commit message uses GitHub's standard merge-PR format, but the
> GitHub repository currently shows **no pull requests** (`gh pr list --state all` returns
> empty). In this lab run the founding was merged with a PR-style **local** merge commit
> rather than through a real PR on the remote. The history reads like a normal PR merge;
> just don't expect to find the PR on GitHub.

## Stage 3 — Plan feature 01 (`e4be43b`, branch `feat/01-skeleton`)

With the substrate in place,
[`plan-feature`](https://github.com/gtrabanco/agentic-workflow/blob/main/skills/plan-feature/SKILL.md)
(routing to its internal `plan-feature-scaffold` step) planned the first roadmap feature. On
a fresh `feat/01-skeleton` branch it:

- wrote **`docs/features/01-skeleton/SPEC.md`** — goal, acceptance criteria (installable
  package, green `ruff`, green `pytest`, a GitHub Actions CI workflow, the stub modules),
  out-of-scope, a tests-first dev-scenario list, and a deploy/rollback note;
- flipped the roadmap row for 01 from `planned` to **`in-progress`**;
- recorded the step in the machine-local `docs/features/.ship-run.log`
  (`01-skeleton | PLAN | done`).

This is the **doc-first** rule in action: the feature is fully specified before any code
exists.

---

## Current state

**Done:** project founded (conventions, roadmap, decisions, docs, templates) and feature 01
planned (SPEC + roadmap flip).

**Not yet built:** no implementation. `src/json2csv/` exists but is **empty** — no
`__init__.py`, `converter.py`, or `cli.py`. There is no `pyproject.toml`, no `tests/`, and no
`.github/workflows/` CI. The verification gate (`ruff check . && pytest`) would currently fail
because there is nothing installable to lint or test.

**Untracked workflow artifacts:**

- `.agents/skills/` — the 14 agentic-workflow skills installed locally (the engine that drives
  the run).
- `skills-lock.json` — a lockfile pinning each skill to `gtrabanco/agentic-workflow` with a
  content hash, so the exact skill set can be restored and verified later.

Neither is committed yet. For a reproducible demo, the usual call is to commit
`skills-lock.json` while git-ignoring the vendored `.agents/skills/` copies.

---

## What's next

The immediate next step is to **execute feature 01**:

```sh
/execute-phase 01 P1     # packaging + ruff + pytest + stub modules + GitHub Actions CI
```

…then review, gate and open a PR:

```sh
/review-change
/audit-pr
gh pr create --base main
```

After 01 merges, the dependency chain continues 02 → 03 → 04 (see
[`ROADMAP.md`](features/ROADMAP.md)). To run the rest unattended:

```sh
/loop /ship-roadmap --continue
```

### Loose ends worth a glance

- **No CI yet.** Acceptance criterion 4 of feature 01 requires a GitHub Actions workflow;
  `.github/workflows/` does not exist. It arrives when 01 is executed.
- **`feat/01-skeleton` has no PR.** The branch is pushed and one commit ahead of `main`;
  opening a PR (or continuing the autopilot) is the next action.
- **Broken documentation-map link.** `CLAUDE.md` lists `docs/features/_TEMPLATE/SPEC.md` as
  the SPEC template, but that file does not exist in the repo. Either vendor the template or
  drop the row.
- **Untracked artifacts.** Decide whether to commit `skills-lock.json` and git-ignore
  `.agents/skills/` (see above).
