import re

from iso639 import Lang

from notebook.bibtex.entry import BibEntry
from notebook.support.unicode import normalize_whitespace

from ..common.entries import generate_entry_name
from ..common.names import name_to_bib_author
from ..common.titles import Titles, split_title
from .model import GoogleBook


def isbn_book_to_bib(book: GoogleBook, isbn: str) -> BibEntry:
    vi = book.volumeInfo
    si = book.searchInfo

    language = Lang(vi.language).name.lower()
    authors = [name_to_bib_author(author) for author in vi.authors]

    year_match = vi.publishedDate and re.match(r'(?P<year>\d{4})', vi.publishedDate)
    year = year_match.group('year') if year_match else ''

    if vi.subtitle is None or vi.subtitle == '':
        titles = split_title(normalize_whitespace(vi.title))
    else:
        titles = Titles(vi.title, vi.subtitle)

    return BibEntry(
        entry_type='book',
        entry_name=generate_entry_name(authors[0], year, titles, language, vi.description, si.textSnippet if si else None),
        authors=authors,
        title=titles.main,
        subtitle=titles.sub,
        language=language,
        date=vi.publishedDate,
        isbn=isbn.format(isbn)
    )
