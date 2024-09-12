import pathlib
from collections.abc import Sequence

import click

from notebook.support.exceptions import exit_gracefully_on_error

from ..common.bulk_format import bulk_format
from ..common.logging import configure_loguru
from .formatting import MatrixFormatter


@click.command()
@click.argument('paths', nargs=-1, type=click.Path(readable=True, dir_okay=False, path_type=pathlib.Path))
@exit_gracefully_on_error
def format_matrices(paths: Sequence[pathlib.Path]) -> None:
    configure_loguru(verbose=False)
    bulk_format(paths, MatrixFormatter)
