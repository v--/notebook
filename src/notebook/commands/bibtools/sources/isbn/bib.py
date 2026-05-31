from typing import TYPE_CHECKING

import stdnum.isbn
from transliterate import translit

from notebook.bibtex import BibEntry
from notebook.commands.bibtools.sources.helpers.dates import extract_year
from notebook.commands.bibtools.sources.helpers.entries import generate_entry_name
from notebook.commands.bibtools.sources.helpers.languages import normalize_language_name
from notebook.commands.bibtools.sources.helpers.names import name_to_bib_author
from notebook.support.unicode import normalize_whitespace


if TYPE_CHECKING:
    from .model import OLBook


def get_language_name(lang_key: str) -> str:
    return normalize_language_name(lang_key.replace('/languages/', ''))


def transliterate_string(string: str, main_language: str) -> str:
    match main_language:
        case 'russian':
            return translit(string, 'ru')

        case 'bulgarian':
            return translit(string, 'bg')

        case _:
            return string


def isbn_book_to_bib(book: OLBook, isbn: str) -> BibEntry:
    bd = book.details

    languages = [get_language_name(lang.key) for lang in bd.languages]
    main_language = languages[0]
    authors = [name_to_bib_author(transliterate_string(author.name, main_language)) for author in bd.authors] if bd.authors else []
    year = extract_year(bd.publish_date)

    title = normalize_whitespace(transliterate_string(bd.title, main_language))
    subtitle = normalize_whitespace(transliterate_string(bd.subtitle, main_language)) if bd.subtitle else None
    publishers = [transliterate_string(publisher, main_language) for publisher in bd.publishers]

    aux_text = list[str]()

    if main_language == 'english' and bd.subjects:
        aux_text.extend(bd.subjects)

    if bd.description and bd.description.type == '/type/text':
        aux_text.append(transliterate_string(bd.description.value, main_language))

    return BibEntry(
        entry_type='book',
        entry_name=generate_entry_name(authors, year, title, languages[0], *aux_text, subtitle=subtitle),
        authors=authors,
        title=title,
        subtitle=subtitle,
        languages=languages,
        date=bd.publish_date,
        publishers=publishers,
        isbn=stdnum.isbn.format(isbn),
    )
