import click

from json2csv import __version__


@click.command()
@click.version_option(__version__)
def main() -> None:
    """Convert JSON to CSV.

    Reads JSON from FILE (or stdin) and writes CSV to stdout.
    """
