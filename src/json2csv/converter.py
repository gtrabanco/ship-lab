"""Pure conversion logic: JSON records → CSV rows."""

import csv
import json
from typing import IO


def _flatten_record(record: dict, prefix: str = "") -> dict:
    result: dict = {}
    for key, value in record.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(_flatten_record(value, full_key))
        else:
            result[full_key] = value
    return result


def convert(records: list[dict], out: IO[str], delimiter: str = ",") -> None:
    """Write *records* as CSV to *out*, flattening nested objects to dot-notation.

    Header: union of all leaf keys in insertion order of first occurrence.
    Missing values written as empty string.
    Empty records list produces no output.
    """
    if not records:
        return

    flat_records = [_flatten_record(r) for r in records]

    # Build ordered union of all keys.
    fieldnames: list[str] = []
    seen: set[str] = set()
    for record in flat_records:
        for key in record:
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)

    if not fieldnames:
        return

    writer = csv.DictWriter(out, fieldnames=fieldnames, extrasaction="ignore",
                            lineterminator="\n", restval="", delimiter=delimiter)
    writer.writeheader()
    writer.writerows({k: _normalize(v) for k, v in row.items()} for row in flat_records)


def _normalize(value: object) -> str | object:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return ""
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    return value
