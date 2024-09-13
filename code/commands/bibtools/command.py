import pathlib
from collections.abc import Sequence

import click

from notebook.exceptions import NotebookCodeError

from ..common.bulk_format import bulk_format
from ..common.exceptions import exit_gracefully_on_exception
from ..common.logging import configure_loguru
from .formatting import BibFormatter
from .sources.arxiv import retrieve_arxiv_entry
from .sources.doi import retrieve_doi_entry
from .sources.isbn import retrieve_isbn_entry


@click.group()
def bibtools() -> None:
    configure_loguru(verbose=False)


@bibtools.command('format')
@click.argument('paths', nargs=-1, type=click.Path(readable=True, dir_okay=False, path_type=pathlib.Path))
@exit_gracefully_on_exception(NotebookCodeError)
def format_(paths: Sequence[pathlib.Path]) -> None:
    bulk_format(BibFormatter, *paths)


@bibtools.group()
def fetch() -> None:
    pass


@fetch.command()
@click.argument('identifier', type=str)
@click.option('--dump-as-fixture', is_flag=True)
@exit_gracefully_on_exception(NotebookCodeError)
def arxiv(identifier: str, *, dump_as_fixture: bool) -> None:
    entry = retrieve_arxiv_entry(identifier, dump_as_fixture=dump_as_fixture)
    click.echo(str(entry), nl=False)


@fetch.command()
@click.argument('identifier', type=str)
@click.option('--dump-as-fixture', is_flag=True)
@exit_gracefully_on_exception(NotebookCodeError)
def isbn(identifier: str, *, dump_as_fixture: bool) -> None:
    entry = retrieve_isbn_entry(identifier, dump_as_fixture=dump_as_fixture)
    click.echo(str(entry), nl=False)


@fetch.command()
@click.argument('identifier', type=str)
@click.option('--print-edition', is_flag=True)
@click.option('--dump-as-fixture', is_flag=True)
@exit_gracefully_on_exception(NotebookCodeError)
def doi(identifier: str, *, print_edition: bool, dump_as_fixture: bool) -> None:
    entry = retrieve_doi_entry(identifier, print_edition=print_edition, dump_as_fixture=dump_as_fixture)
    click.echo(str(entry), nl=False)
