import click
import pathlib

from .formatting import BibFormatter
from ..common.bulk_format import bulk_format


@click.command()
@click.argument('path', type=str)
def format_matrices(path: str):
    bulk_format(
        pathlib.Path(path),
        '**/*.bib',
        BibFormatter
    )
