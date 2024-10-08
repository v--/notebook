import stdnum

from notebook.bibtex.entry import BibEntry

from ..common.dates import extract_year
from ..common.entries import generate_entry_name
from ..common.languages import normalize_language_name
from ..common.names import name_to_bib_author
from ..common.titles import construct_titles
from .model import GoogleBook


def isbn_book_to_bib(book: GoogleBook, isbn: str) -> BibEntry:
    vi = book.volume_info
    si = book.search_info

    language = normalize_language_name(vi.language)
    authors = [name_to_bib_author(author) for author in vi.authors] if vi.authors else []
    year = extract_year(vi.published_date)
    titles = construct_titles(vi.title, vi.subtitle)

    return BibEntry(
        entry_type='book',
        entry_name=generate_entry_name(authors, year, titles, language, vi.description, si.text_snippet if si else None),
        authors=authors,
        title=titles.main,
        subtitle=titles.sub,
        languages=[language],
        date=vi.published_date,
        isbn=stdnum.isbn.format(isbn)
    )
