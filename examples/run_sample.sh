#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT="$SCRIPT_DIR/input.json"

echo "=== 1/3  comma-delimited (default) ==="
json2csv "$INPUT" -o "$SCRIPT_DIR/out_comma.csv"
echo "Written: examples/out_comma.csv"

echo ""
echo "=== 2/3  tab-delimited ==="
json2csv "$INPUT" -d $'\t' -o "$SCRIPT_DIR/out_tab.csv"
echo "Written: examples/out_tab.csv"

echo ""
echo "=== 3/3  stdin pipe (comma, stdout) ==="
json2csv < "$INPUT" > "$SCRIPT_DIR/out_stdin.csv"
echo "Written: examples/out_stdin.csv"

echo ""
echo "Done. Open the CSV files in a spreadsheet and verify:"
echo "  out_comma.csv — address.city and address.country as separate columns;"
echo "                  tags column contains a JSON-encoded string e.g. [\"python\", \"data\"]"
echo "  out_tab.csv   — same columns, tab-separated; opens as a table in spreadsheet apps"
echo "  out_stdin.csv — identical to out_comma.csv (stdin path regression check)"
