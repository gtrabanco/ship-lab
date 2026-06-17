# Ship Lab

**A live demo of [agentic-workflow](https://github.com/gtrabanco/agentic-workflow).**

This repository is a worked example: a real command-line tool — **json2csv** — being
built end to end by AI agents running the agentic-workflow skills. Its git history *is*
the workflow running: each commit was produced by a skill — founding the project, then
planning, implementing, reviewing and shipping one feature per PR. Three features and two
fixes are merged; one feature remains. Read the repo top to bottom and you are reading the
workflow's output.

> agentic-workflow — *"a reusable set of agent skills that run a disciplined, doc-driven
> workflow for building software with agents — from idea/issue to a reviewed, classified,
> merge-ready change."*

---

## What's being built

**json2csv** — a Python 3.11+ / [Click](https://click.palletsprojects.com/) CLI that reads
JSON from a file or stdin and writes CSV to a file or stdout. Small on purpose: the point
is to show the *workflow*, not the product.

## The workflow, in one loop

The skills turn an idea (or a GitHub issue) into a merge-ready PR through the same loop
every time — plan, build one phase at a time, review, gate, ship:

```sh
/plan-feature "<idea>"        # idea/issue → scoped SPEC + roadmap entry
/execute-phase <NN> <phase>   # one phase, gate-verified, one commit
/review-change                # findings classified → fix-now / postpone / ignore
/audit-pr                     # merge gate: MERGE-READY or a list of blockers
gh pr create --base main
```

Doc-first and stack-agnostic: the rules live in [`CLAUDE.md`](CLAUDE.md), the plan lives in
[`docs/features/ROADMAP.md`](docs/features/ROADMAP.md), and code only appears once the plan
exists. The verification gate — `ruff check . && pytest` — must be green before any commit.

## Where this demo is right now

The workflow has **founded** the project and shipped the first three features — each one
planned to a SPEC, implemented, reviewed, gated and merged through its own PR. Two
review-born fixes were triaged and merged the same way. One feature (nested-object flatten)
remains on the roadmap.

| #  | Feature                                   | Status                                       |
|----|-------------------------------------------|----------------------------------------------|
| 01 | skeleton (packaging, ruff, pytest, CI)    | 🟢 done                                       |
| 02 | basic JSON → CSV                          | 🟢 done                                       |
| 03 | `--delimiter` flag                        | 🟢 done                                       |
| 04 | nested-object flatten                     | ⚪ planned                                     |

The full step-by-step story — every commit mapped to the skill that produced it — is in
**[docs/PROCESS.md](docs/PROCESS.md)**.

## Try the sample

A ready-to-run sample lives in [`examples/`](examples/). It lets you verify the
behaviours that automated tests cannot confirm — column alignment, tab-delimited
rendering, and JSON list-cell display.

**1. Install the package** (once):

```sh
pip install -e .
```

**2. Run the script:**

```sh
bash examples/run_sample.sh
```

This writes three files (git-ignored so every user gets their own copy):

| File | What to verify |
|---|---|
| `examples/out_comma.csv` | 👤 `address.city` and `address.country` appear as **separate columns**; `tags` column contains a JSON-encoded string (e.g. `["python", "data"]`) — paste the cell value into `python -c "import json,sys; print(json.loads(sys.argv[1]))" '["python","data"]'` to confirm it round-trips |
| `examples/out_tab.csv` | 👤 Open in a spreadsheet app — all columns must align cleanly with no merged or split cells |
| `examples/out_stdin.csv` | Identical to `out_comma.csv` (stdin path regression) |

## Run the workflow yourself

Install the skills into any agent that reads Markdown skills (Claude Code, Cursor, and 70+
others):

```sh
npx skills add gtrabanco/agentic-workflow      # all skills
npx skills list                                # see what you got
```

Or scaffold a fresh project from the same doc template this repo started from:

```sh
npx degit gtrabanco/agentic-workflow/template my-project
```

Then point an agent at it and run `/ship-roadmap` to autopilot the whole thing, or drive it
one skill at a time with the loop above.

---

Built with [agentic-workflow](https://github.com/gtrabanco/agentic-workflow) · skills are MIT-licensed.
