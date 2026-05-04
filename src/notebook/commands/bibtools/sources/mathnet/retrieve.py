from typing import TYPE_CHECKING

from .bib import mathnet_entry_to_bib
from .fetch import fetch_mathnet_html
from .model import parse_mathnet_html


if TYPE_CHECKING:
    from notebook.bibtex import BibEntry


def retrieve_mathnet_entry(identifier: str, *, english: bool, dump_as_fixture: bool) -> BibEntry:
    html = fetch_mathnet_html(identifier, dump_as_fixture=dump_as_fixture)
    res = parse_mathnet_html(html, english=english)
    return mathnet_entry_to_bib(res, identifier, english=english)
