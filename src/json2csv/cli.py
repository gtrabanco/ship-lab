import json
from typing import IO

import click

from json2csv import __version__
from json2csv.converter import convert


@click.command()
@click.version_option(__version__)
@click.argument("input_file", type=click.File("r", encoding="utf-8"), default="-",
                metavar="[FILE]")
@click.option("-o", "--output", "output_file", type=click.File("w", encoding="utf-8"),
              default="-", show_default=True, help="Output CSV file (default: stdout).")
@click.option("-d", "--delimiter", default=",", show_default=True,
              metavar="CHAR", help="Field delimiter character.")
def main(input_file: IO[str], output_file: IO[str], delimiter: str) -> None:
    """Convert JSON to CSV.

    Reads a JSON array of objects from FILE (or stdin) and writes CSV to
    stdout (or --output).
    """
    if len(delimiter) != 1:
        raise click.ClickException("delimiter must be a single character.")
    if delimiter in '"\r\n':
        raise click.ClickException("delimiter cannot be a quote or newline character.")

    try:
        records = json.load(input_file)
    except json.JSONDecodeError as exc:
        raise click.ClickException(f"invalid JSON — {exc}") from exc

    if not isinstance(records, list):
        raise click.ClickException("expected a JSON array at the top level.")

    if records and not all(isinstance(r, dict) for r in records):
        raise click.ClickException("expected a JSON array of objects.")

    convert(records, output_file, delimiter=delimiter)
