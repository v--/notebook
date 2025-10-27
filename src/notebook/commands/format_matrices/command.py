import pathlib
from collections.abc import Sequence

import click

from ...exceptions import NotebookError
from ...latex.format_matrices import format_tex_matrices
from ..common.exception_handling import exit_gracefully_on_exception
from ..common.formatting import FormatterContextManager
from ..common.logging import configure_loguru


@click.command()
@click.argument('paths', nargs=-1, type=click.Path(readable=True, dir_okay=False, path_type=pathlib.Path))
@exit_gracefully_on_exception(NotebookError)
def format_matrices(paths: Sequence[pathlib.Path]) -> None:
    configure_loguru(verbose=False)

    for path in paths:
        with FormatterContextManager(path) as context:
            context.dest.write(format_tex_matrices(context.src.read()))
