import pathlib

import click

from ..common.bulk_format import bulk_format
from .formatting import BibFormatter


@click.command()
@click.argument('path', type=str)
def format_bibliography(path: str) -> None:
    bulk_format(
        pathlib.Path(path),
        '**/*.bib',
        BibFormatter
    )
