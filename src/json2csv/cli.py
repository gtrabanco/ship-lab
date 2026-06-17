import json
import sys
from typing import IO

import click

from json2csv import __version__
from json2csv.converter import convert


@click.command()
@click.version_option(__version__)
@click.argument("input_file", type=click.File("r"), default="-", metavar="[FILE]")
@click.option("-o", "--output", "output_file", type=click.File("w"),
              default="-", show_default=True, help="Output CSV file (default: stdout).")
def main(input_file: IO[str], output_file: IO[str]) -> None:
    """Convert JSON to CSV.

    Reads a JSON array of objects from FILE (or stdin) and writes CSV to
    stdout (or --output).
    """
    try:
        records = json.load(input_file)
    except json.JSONDecodeError as exc:
        click.echo(f"Error: invalid JSON — {exc}", err=True)
        sys.exit(1)

    if not isinstance(records, list):
        click.echo("Error: expected a JSON array at the top level.", err=True)
        sys.exit(1)

    convert(records, output_file)
