
from notebook.bibtex.entry import BibEntry
from notebook.support.unicode import normalize_whitespace

from ..common.dates import extract_year
from ..common.entries import generate_entry_name
from ..common.languages import normalize_language_name
from ..common.names import name_to_bib_author
from ..common.titles import Titles, split_title
from .model import GoogleBook


def isbn_book_to_bib(book: GoogleBook, isbn: str) -> BibEntry:
    vi = book.volume_info
    si = book.search_info

    language = normalize_language_name(vi.language)
    authors = [name_to_bib_author(author) for author in vi.authors]

    year = extract_year(vi.published_date)

    if vi.subtitle is None or vi.subtitle == '':
        titles = split_title(normalize_whitespace(vi.title))
    else:
        titles = Titles(vi.title, vi.subtitle)

    return BibEntry(
        entry_type='book',
        entry_name=generate_entry_name(authors[0], year, titles, language, vi.description, si.text_snippet if si else None),
        authors=authors,
        title=titles.main,
        subtitle=titles.sub,
        language=language,
        date=vi.published_date,
        isbn=isbn.format(isbn)
    )
