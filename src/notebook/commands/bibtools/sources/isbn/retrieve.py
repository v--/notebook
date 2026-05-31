import json
from typing import TYPE_CHECKING

from notebook.commands.bibtools.exceptions import BibToolsError

from .bib import isbn_book_to_bib
from .fetch import fetch_isbn_json
from .fixtures import get_isbn_fixture_path
from .model import parse_isbn_json


if TYPE_CHECKING:
    from notebook.bibtex import BibEntry


def retrieve_isbn_entry(identifier: str, *, dump_as_fixture: bool) -> BibEntry:
    json_body = fetch_isbn_json(identifier)
    res = json.loads(json_body)
    book_json = res.get(f'ISBN:{identifier}')

    if book_json is None:
        raise BibToolsError(f'No books with ISBN {identifier} found')

    if dump_as_fixture:
        with get_isbn_fixture_path(identifier).open('w') as file:
            json.dump(book_json, file)

    book = parse_isbn_json(book_json)
    return isbn_book_to_bib(book, identifier)
