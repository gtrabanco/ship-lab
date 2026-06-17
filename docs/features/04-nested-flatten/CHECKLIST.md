# Checklist — 04 nested-flatten

**Gate:** `ruff check . && pytest` — 29/29 ✓

| Item | Status |
|---|---|
| Schema migration | n/a |
| Core layer has no outer-layer imports | ✓ (`converter.py` imports only stdlib: `csv`, `json`) |
| `cli.py` unchanged | ✓ |
| Tests pass | ✓ 29/29 |
| Ruff green | ✓ |
| UI strings localized | n/a (CLI) |
| User-facing limitations disclosed | ✓ (list cells, fixed `.` separator — in SPEC Out of scope) |
| New deps pinned | n/a (only stdlib additions) |

## Human-verification (confirmed 2026-06-17)

- [x] 👤 Flattened CSV (`address.city`-style headers) opens cleanly in a spreadsheet app — columns align correctly _(human visual check)_
- [x] 👤 JSON-encoded list cell (e.g. `"[""python"", ""data""]"`) displays and re-imports acceptably _(human visual check)_

## Decisions not in SPEC

- Added `if not fieldnames: return` guard so a record that flattens to an empty
  dict (e.g. `{"a": {}}`) produces no output instead of a headerless empty line.
- `_normalize` extended with `isinstance(value, list)` → `json.dumps` branch;
  applies to list values at any nesting depth, including flat input that happens
  to carry list values (additive, no existing test uses list leaf values).
