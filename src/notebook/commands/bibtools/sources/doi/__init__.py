from .....bibtex import BibEntry
from ..common.url_template import UrlTemplate
from .bib import doi_data_to_bib
from .fetch import fetch_doi_json
from .model import parse_doi_json


def retrieve_doi_entry(identifier: str, *, print_edition: bool, dump_as_fixture: bool) -> BibEntry:
    json_body = fetch_doi_json(identifier, dump_as_fixture=dump_as_fixture)
    data = parse_doi_json(json_body)
    return doi_data_to_bib(data, identifier, print_edition=print_edition)
