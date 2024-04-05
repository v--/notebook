import pathlib

import click

from ..common.bulk_format import bulk_format
from .formatting import MatrixFormatter


@click.command()
@click.argument('path', type=str)
def format_matrices(path: str) -> None:
    bulk_format(
        pathlib.Path(path),
        '**/*.tex',
        MatrixFormatter
    )
