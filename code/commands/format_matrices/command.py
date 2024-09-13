import pathlib
from collections.abc import Sequence

import click

from notebook.exceptions import NotebookCodeError

from ..common.bulk_format import bulk_format
from ..common.exceptions import exit_gracefully_on_exception
from ..common.logging import configure_loguru
from .formatting import MatrixFormatter


@click.command()
@click.argument('paths', nargs=-1, type=click.Path(readable=True, dir_okay=False, path_type=pathlib.Path))
@exit_gracefully_on_exception(NotebookCodeError)
def format_matrices(paths: Sequence[pathlib.Path]) -> None:
    configure_loguru(verbose=False)
    bulk_format(MatrixFormatter, *paths)
