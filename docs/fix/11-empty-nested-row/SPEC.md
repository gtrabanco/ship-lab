# SPEC — fix/11 empty-nested-row

**Issue:** #11 · **Branch:** fix/11-empty-nested-row · **Status:** in-progress

## Problem

When a record whose only content is an empty nested object (e.g. `{"a": {}}`)
appears alongside populated records, it flattens to an empty dict `{}` and
`convert()` still emits a CSV row — rendered as a quoted-empty field (`""`) in a
single-column output. Users see a stray blank row in their spreadsheet.

```
printf '[{"a":{}},{"b":1}]' | json2csv
b
""        <- unwanted
1
```

## Fix

In `convert()`, skip records that flatten to an empty dict before writing rows:
filter the `writerows` generator with `if row`. A record that flattens to a
non-empty dict (e.g. `{"a": {}, "b": 1}` → `{"b": 1}`) is unaffected.

## Acceptance criteria

1. `[{"a":{}},{"b":1}]` produces `b\n1` — no `""` row.
2. Sole-record empty case `[{"a":{}}]` still produces empty output (unchanged).
3. A record mixing empty and populated keys (`{"a":{},"b":1}`) still emits its row.
4. `ruff check . && pytest` exits 0.

## Out of scope

Any other flattening behaviour; array index expansion; the fixed `.` separator.
