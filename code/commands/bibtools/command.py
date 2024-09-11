import pathlib

import click

from notebook.support.exceptions import exit_gracefully_on_error

from ..common.bulk_format import bulk_format
from .formatting import BibFormatter
from .sources.arxiv import retrieve_arxiv_entry
from .sources.doi import retrieve_doi_entry
from .sources.isbn import retrieve_isbn_entry


@click.group()
def bibtools() -> None:
    pass


@bibtools.command()
@click.argument('path', type=str)
def format(path: str) -> None:  # noqa: A001
    bulk_format(
        pathlib.Path(path),
        '**/*.bib',
        BibFormatter
    )


@bibtools.group()
def fetch() -> None:
    pass


@fetch.command()
@click.argument('identifier', type=str)
@click.option('--dump-as-fixture', is_flag=True)
@exit_gracefully_on_error
def arxiv(identifier: str, *, dump_as_fixture: bool) -> None:
    entry = retrieve_arxiv_entry(identifier, dump_as_fixture=dump_as_fixture)
    click.echo(str(entry), nl=False)


@fetch.command()
@click.argument('identifier', type=str)
@click.option('--dump-as-fixture', is_flag=True)
@exit_gracefully_on_error
def isbn(identifier: str, *, dump_as_fixture: bool) -> None:
    entry = retrieve_isbn_entry(identifier, dump_as_fixture=dump_as_fixture)
    click.echo(str(entry), nl=False)


@fetch.command()
@click.argument('identifier', type=str)
@click.option('--print-edition', is_flag=True)
@click.option('--dump-as-fixture', is_flag=True)
@exit_gracefully_on_error
def doi(identifier: str, *, print_edition: bool, dump_as_fixture: bool) -> None:
    entry = retrieve_doi_entry(identifier, print_edition=print_edition, dump_as_fixture=dump_as_fixture)
    click.echo(str(entry), nl=False)
