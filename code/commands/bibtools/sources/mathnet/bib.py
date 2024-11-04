from notebook.bibtex.entry import BibEntry
from notebook.support.unicode import normalize_whitespace

from ... import url_templates
from ..common.dates import extract_year
from ..common.entries import generate_entry_name
from ..common.names import name_to_bib_author
from ..common.pages import normalize_pages
from .model import MathNetEntry


def mathnet_entry_to_bib(entry: MathNetEntry, identifier: str, *, english: bool) -> BibEntry:
    language = 'english' if english else 'russian'
    authors = [name_to_bib_author(author.strip()) for author in entry.by.split(',')]
    year = extract_year(entry.yr)
    title = normalize_whitespace(entry.paper)

    return BibEntry(
        entry_type='article',
        entry_name=generate_entry_name(authors, year, title, language),
        authors=authors,
        title=title,
        languages=[language],
        date=year,
        journal=entry.jour,
        series=entry.serial,
        publisher=entry.publ,
        volume=entry.vol,
        issue=entry.issue,
        pages=normalize_pages(entry.pages) if entry.pages else None,
        mathnet=identifier,
        doi=url_templates.clean_identifier(entry.crossref, url_templates.doi),
        mathscinet=url_templates.clean_identifier(entry.mathscinet, url_templates.mathscinet),
        zbmath=url_templates.clean_identifier(entry.zmath, url_templates.zbmath),
        scopus=url_templates.clean_identifier(entry.scopus, url_templates.scopus)
    )
