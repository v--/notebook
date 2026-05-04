from typing import TYPE_CHECKING

from .bib import stackexchange_entry_to_bib
from .fetch import fetch_stackexchange_html
from .model import parse_stackexchange_html


if TYPE_CHECKING:
    from notebook.bibtex import BibEntry


def retrieve_stackexchange_entry(identifier: str, *, dump_as_fixture: bool) -> BibEntry:
    html = fetch_stackexchange_html(identifier, dump_as_fixture=dump_as_fixture)
    res = parse_stackexchange_html(html)
    return stackexchange_entry_to_bib(res, identifier)
