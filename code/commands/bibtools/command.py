import pathlib

import click

from notebook.support.exceptions import exit_gracefully_on_error

from ..common.bulk_format import bulk_format
from .exceptions import BibToolsError
from .formatting import BibFormatter
from .sources.arxiv.bib import arxiv_entry_to_bib
from .sources.arxiv.fetch import fetch_arxiv_xml
from .sources.arxiv.model import parse_arxiv_xml
from .sources.doi.bib import doi_data_to_bib
from .sources.doi.fetch import fetch_doi_json
from .sources.doi.model import parse_doi_json
from .sources.isbn.bib import isbn_book_to_bib
from .sources.isbn.fetch import fetch_isbn_json
from .sources.isbn.model import parse_isbn_json


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
    xml_body = fetch_arxiv_xml(identifier, dump_as_fixture=dump_as_fixture)
    feed = parse_arxiv_xml(xml_body)

    if len(feed.entries) == 0:
        raise BibToolsError('No entries found')

    if len(feed.entries) > 1:
        raise BibToolsError('Too many entries')

    entry = arxiv_entry_to_bib(feed.entries[0], identifier)
    click.echo(str(entry), nl=False)


@fetch.command()
@click.argument('identifier', type=str)
@click.option('--dump-as-fixture', is_flag=True)
@exit_gracefully_on_error
def isbn(identifier: str, *, dump_as_fixture: bool) -> None:
    json_body = fetch_isbn_json(identifier, dump_as_fixture=dump_as_fixture)
    res = parse_isbn_json(json_body)

    if len(res.items) == 0:
        raise BibToolsError('No books found')

    if len(res.items) > 1:
        raise BibToolsError('Too many books found')

    entry = isbn_book_to_bib(res.items[0], identifier)
    click.echo(str(entry), nl=False)


@fetch.command()
@click.argument('identifier', type=str)
@click.option('--print-edition', is_flag=True)
@click.option('--dump-as-fixture', is_flag=True)
@exit_gracefully_on_error
def doi(identifier: str, *, print_edition: bool, dump_as_fixture: bool) -> None:
    json_body = fetch_doi_json(identifier, dump_as_fixture=dump_as_fixture)
    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, identifier, print_edition=print_edition)
    click.echo(str(entry), nl=False)
