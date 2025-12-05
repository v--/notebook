import stdnum

from .....bibtex import BibEntry
from .....support.unicode import normalize_whitespace
from ..common.dates import extract_year
from ..common.entries import generate_entry_name
from ..common.languages import normalize_language_name
from ..common.names import name_to_bib_author
from .model import GoogleBook


def isbn_book_to_bib(book: GoogleBook, isbn: str) -> BibEntry:
    vi = book.volume_info
    si = book.search_info

    language = normalize_language_name(vi.language)
    authors = [name_to_bib_author(author) for author in vi.authors] if vi.authors else []
    year = extract_year(vi.published_date)

    title = normalize_whitespace(vi.title)
    subtitle = normalize_whitespace(vi.subtitle) if vi.subtitle else None

    return BibEntry(
        entry_type='book',
        entry_name=generate_entry_name(authors, year, title, language, vi.description, si.text_snippet if si else None, subtitle=subtitle),
        authors=authors,
        title=title,
        subtitle=subtitle or None,
        languages=[language],
        date=vi.published_date,
        isbn=stdnum.isbn.format(isbn)
    )
