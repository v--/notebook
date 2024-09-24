from notebook.bibtex.entry import BibEntry

from ...exceptions import BibToolsError
from .bib import mathnet_entry_to_bib
from .fetch import fetch_mathnet_html
from .model import parse_mathnet_html


def retrieve_mathnet_entry(identifier: str, *, english: bool, dump_as_fixture: bool) -> BibEntry:
    html = fetch_mathnet_html(identifier, dump_as_fixture=dump_as_fixture)
    res = parse_mathnet_html(html, english=english)
    return mathnet_entry_to_bib(res, identifier, english=english)
