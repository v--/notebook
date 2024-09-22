import pathlib
from collections.abc import Sequence

import click

from notebook.exceptions import NotebookCodeError

from ..common.exceptions import exit_gracefully_on_exception
from ..common.formatting import FormatterContextManager
from ..common.logging import configure_loguru
from .formatting import adjust_entry, read_entries, write_entries
from .sources.arxiv import retrieve_arxiv_entry
from .sources.doi import retrieve_doi_entry
from .sources.isbn import retrieve_isbn_entry
from .sources.mathnet import retrieve_mathnet_entry


@click.group()
def bibtools() -> None:
    configure_loguru(verbose=False)


@bibtools.command('format')
@click.argument('paths', nargs=-1, type=click.Path(readable=True, dir_okay=False, path_type=pathlib.Path))
@exit_gracefully_on_exception(NotebookCodeError)
def format_(paths: Sequence[pathlib.Path]) -> None:
    for path in paths:
        with FormatterContextManager(path) as context:
            entries = list(read_entries(context.src))

            for i, entry in enumerate(entries):
                logger = context.logger.bind(logger=path.stem + ':' + entry.entry_name)
                entries[i] = adjust_entry(entry, logger)

            write_entries(
                sorted(entries, key=lambda entry: entry.entry_name),
                context.dest
            )


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
@click.option('--print', is_flag=True)
@click.option('--dump-as-fixture', is_flag=True)
@exit_gracefully_on_exception(NotebookCodeError)
def doi(identifier: str, *, print: bool, dump_as_fixture: bool) -> None:
    entry = retrieve_doi_entry(identifier, print_edition=print, dump_as_fixture=dump_as_fixture)
    click.echo(str(entry), nl=False)


@fetch.command()
@click.argument('identifier', type=str)
@click.option('--english', is_flag=True)
@click.option('--dump-as-fixture', is_flag=True)
@exit_gracefully_on_exception(NotebookCodeError)
def mathnet(identifier: str, *, english: bool, dump_as_fixture: bool) -> None:
    entry = retrieve_mathnet_entry(identifier, english=english, dump_as_fixture=dump_as_fixture)
    click.echo(str(entry), nl=False)
