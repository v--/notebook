import pathlib

import click

from ..common.bulk_format import bulk_format
from .formatting import BibFormatter


@click.group()
def bibtools() -> None:
    pass


@bibtools.command()
@click.argument('path', type=str)
def format(path: str) -> None:  # noqa: A001
    bulk_format(
        pathlib.Path(path),
        '**/*.bib',
        BibFormatter
    )
