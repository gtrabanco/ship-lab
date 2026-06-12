# Workflow — json2csv

Skills-driven, doc-first workflow. Full tutorial:
[agentic-workflow docs](https://github.com/gtrabanco/agentic-workflow/tree/main/docs/workflow).

## Quick reference

```sh
# Build a feature
/plan-feature "<idea>"          # or /plan-feature <N>  or  /plan-feature --next
/execute-phase <NN> <phase>     # one phase, gate-verified, one commit
/review-change                  # findings classified → table + manual checks
/audit-pr                       # merge gate: ready or blockers
gh pr create --base main

# Handle an issue
/triage-issue <N>

# Autopilot (whole roadmap)
/ship-roadmap                   # founding interview (done — see SHIP_DECISIONS.md)
/loop /ship-roadmap --continue  # ships feature by feature
```

Verification gate: `ruff check . && pytest`
