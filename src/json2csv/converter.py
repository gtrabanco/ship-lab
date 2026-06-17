"""Pure conversion logic: JSON records → CSV rows."""

import csv
from typing import IO


def convert(records: list[dict], out: IO[str]) -> None:
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
                            lineterminator="\n", restval="")
    writer.writeheader()
    writer.writerows(records)
