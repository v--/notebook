import pathlib
lazy from collections.abc import Sequence

import click

from notebook.commands.common.exception_handling import with_cli_exception_handler
from notebook.commands.common.formatting import FormatterContextManager
from notebook.commands.common.logging import setup_logging
from notebook.exceptions import NotebookError
from notebook.latex.format_matrices import format_tex_matrices


@click.command()
@click.argument('paths', nargs=-1, type=click.Path(readable=True, dir_okay=False, path_type=pathlib.Path))
def format_matrices(paths: Sequence[pathlib.Path]) -> None:
    setup_logging(verbose=False, log_subject=False)

    for path in paths:
        with FormatterContextManager(path) as context, with_cli_exception_handler(NotebookError):
            context.dest.write(format_tex_matrices(context.src.read()))
