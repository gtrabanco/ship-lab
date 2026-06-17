"""Pure conversion logic: JSON records → CSV rows."""

import csv
from typing import IO


def convert(records: list[dict], out: IO[str], delimiter: str = ",") -> None:
    """Write *records* (list of flat dicts) as CSV to *out*.

    Header: union of all keys in insertion order of first occurrence.
    Missing values written as empty string.
    Empty records list produces no output.
    """
    if not records:
        return

    # Build ordered union of all keys.
    fieldnames: list[str] = []
    seen: set[str] = set()
    for record in records:
        for key in record:
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)

    writer = csv.DictWriter(out, fieldnames=fieldnames, extrasaction="ignore",
                            lineterminator="\n", restval="", delimiter=delimiter)
    writer.writeheader()
    writer.writerows({k: _normalize(v) for k, v in row.items()} for row in records)


def _normalize(value: object) -> str | object:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return ""
    return value
