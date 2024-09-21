from notebook.bibtex.entry import BibEntry
from notebook.support.unicode import normalize_whitespace

from ..common.dates import extract_year
from ..common.entries import generate_entry_name
from ..common.names import name_to_bib_author
from ..common.titles import split_title
from .model import MathNetEntry


def mathnet_entry_to_bib(entry: MathNetEntry, *, english: bool) -> BibEntry:
    language = 'english' if english else 'russian'
    authors = [name_to_bib_author(author.strip()) for author in entry.by.split(',')]
    year = extract_year(entry.yr)
    titles = split_title(normalize_whitespace(entry.paper))

    return BibEntry(
        entry_type='article',
        entry_name=generate_entry_name(authors[0], year, titles, language),
        authors=authors,
        title=titles.main,
        subtitle=titles.sub,
        language=language,
        date=year,
        journal=entry.jour,
        series=entry.serial,
        publisher=entry.publ,
        volume=entry.vol,
        issue=entry.issue,
        pages=entry.pages,
        url=entry.mathnet,
        doi=entry.crossref,
        mathscinet=entry.mathscinet,
        zmath=entry.zmath,
        scopus=entry.scopus
    )
