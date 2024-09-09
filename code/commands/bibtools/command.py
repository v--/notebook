import pathlib

import click

from notebook.support.exceptions import exit_gracefully_on_error

from ..common.bulk_format import bulk_format
from .exceptions import BibToolsError
from .formatting import BibFormatter
from .sources.arxiv.bib import arxiv_entry_to_bib
from .sources.arxiv.fetch import fetch_arxiv_xml
from .sources.arxiv.model import parse_arxiv_xml


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

    entry = arxiv_entry_to_bib(feed.entries[0])
    click.echo(str(entry), nl=False)


# @fetch.command()
# @click.argument('identifier', type=str)
# def doi(identifier: str) -> None:
#     pass


# @fetch.command()
# @click.argument('identifier', type=str)
# def isbn(identifier: str) -> None:
#     pass
