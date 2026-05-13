import contextlib
from typing import TYPE_CHECKING

import click


if TYPE_CHECKING:
    from collections.abc import Generator


@contextlib.contextmanager
def with_cli_exception_handler(*exceptions: type[Exception]) -> Generator[None]:
    """Set up an handler that pretty prints viat exceptions."""
    try:
        yield
    except exceptions as err:
        raise click.ClickException(str(err)) from err
