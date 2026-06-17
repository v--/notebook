import contextlib
lazy from collections.abc import Generator

import click


@contextlib.contextmanager
def with_cli_exception_handler(*exceptions: type[Exception]) -> Generator[None]:
    """Set up an handler that pretty prints certain exceptions."""
    try:
        yield
    except exceptions as err:
        raise click.ClickException(str(err)) from err
