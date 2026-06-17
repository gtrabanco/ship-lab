#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INPUT="$SCRIPT_DIR/input.json"

# Resolve json2csv: prefer the repo's .venv, fall back to PATH.
if [ -x "$REPO_ROOT/.venv/bin/json2csv" ]; then
    JSON2CSV="$REPO_ROOT/.venv/bin/json2csv"
elif command -v json2csv >/dev/null 2>&1; then
    JSON2CSV="json2csv"
else
    echo "Error: json2csv not found." >&2
    echo "Run 'pip install -e .' from the repo root first." >&2
    exit 1
fi

echo "=== 1/3  comma-delimited (default) ==="
"$JSON2CSV" "$INPUT" -o "$SCRIPT_DIR/out_comma.csv"
echo "Written: examples/out_comma.csv"

echo ""
echo "=== 2/3  tab-delimited ==="
"$JSON2CSV" "$INPUT" -d $'\t' -o "$SCRIPT_DIR/out_tab.csv"
echo "Written: examples/out_tab.csv"

echo ""
echo "=== 3/3  stdin pipe (comma, stdout) ==="
"$JSON2CSV" < "$INPUT" > "$SCRIPT_DIR/out_stdin.csv"
echo "Written: examples/out_stdin.csv"

echo ""
echo "Done. Open the CSV files in a spreadsheet and verify:"
echo "  out_comma.csv — address.city and address.country as separate columns;"
echo "                  tags column contains a JSON-encoded string e.g. [\"python\", \"data\"]"
echo "  out_tab.csv   — same columns, tab-separated; opens as a table in spreadsheet apps"
echo "  out_stdin.csv — identical to out_comma.csv (stdin path regression check)"
