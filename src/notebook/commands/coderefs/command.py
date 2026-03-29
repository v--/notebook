import click

from ..common.logging import configure_loguru


@click.group()
def coderefs() -> None:
    configure_loguru(verbose=False)
