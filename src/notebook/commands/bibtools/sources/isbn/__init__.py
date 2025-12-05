from .....bibtex import BibEntry
from ...exceptions import BibToolsError
from .bib import isbn_book_to_bib
from .fetch import fetch_isbn_json
from .model import parse_isbn_json


def retrieve_isbn_entry(identifier: str, *, dump_as_fixture: bool) -> BibEntry:
    json_body = fetch_isbn_json(identifier, dump_as_fixture=dump_as_fixture)
    res = parse_isbn_json(json_body)

    if len(res.items) == 0:
        raise BibToolsError('No books found')

    if len(res.items) > 1:
        raise BibToolsError('Too many books found')

    return isbn_book_to_bib(res.items[0], identifier)
