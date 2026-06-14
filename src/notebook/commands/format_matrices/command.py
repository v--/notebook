import logging
import pathlib
from typing import TYPE_CHECKING

import click

from notebook.commands.common.exception_handling import with_cli_exception_handler
from notebook.commands.common.formatting import FormatterContextManager
from notebook.commands.common.logging import SubjectLoggerHandler
from notebook.exceptions import NotebookError
from notebook.latex.format_matrices import format_tex_matrices


if TYPE_CHECKING:
    from collections.abc import Sequence


@click.command()
@click.argument('paths', nargs=-1, type=click.Path(readable=True, dir_okay=False, path_type=pathlib.Path))
@click.pass_context
def format_matrices(ctx: click.Context, paths: Sequence[pathlib.Path]) -> None:
    ctx.with_resource(with_cli_exception_handler(NotebookError))

    base_logger = logging.getLogger('notebook.commands')
    base_logger.setLevel(logging.INFO)
    base_logger.addHandler(SubjectLoggerHandler())

    for path in paths:
        with FormatterContextManager(path) as context:
            context.dest.write(format_tex_matrices(context.src.read()))
