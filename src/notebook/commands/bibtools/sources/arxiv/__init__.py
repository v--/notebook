from .....bibtex import BibEntry
from ...exceptions import BibToolsError
from ..common.url_template import UrlTemplate
from .bib import arxiv_entry_to_bib
from .fetch import fetch_arxiv_xml
from .model import parse_arxiv_xml


def retrieve_arxiv_entry(identifier: str, *, dump_as_fixture: bool) -> BibEntry:
    xml_body = fetch_arxiv_xml(identifier, dump_as_fixture=dump_as_fixture)
    feed = parse_arxiv_xml(xml_body)

    if len(feed.entries) == 0:
        raise BibToolsError('No entries found')

    if len(feed.entries) > 1:
        raise BibToolsError('Too many entries')

    return arxiv_entry_to_bib(feed.entries[0], identifier)
