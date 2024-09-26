from collections.abc import Iterable, Sequence

from nameparser import HumanName
from stdnum import isbn, issn

from notebook.bibtex.author import BibAuthor
from notebook.bibtex.entry import BibEntry, BibEntryType
from notebook.exceptions import UnreachableException

from ..common.entries import generate_entry_name
from ..common.languages import normalize_language_name
from ..common.pages import normalize_pages
from ..common.titles import construct_titles
from .model import DoiAuthor, DoiData, DoiDateTime, DoiIsbn


def doi_authors_to_bib(authors: Sequence[DoiAuthor]) -> Iterable[BibAuthor]:
    for author in authors:
        names = HumanName(first=author.given, last=author.family)

        if len(str(names)) > 0:
            yield BibAuthor(full_name=str(names))


def choose_doi_datetime(data: DoiData, *, print_edition: bool) -> DoiDateTime | None:
    if print_edition and data.published_print:
        return data.published_print

    if not print_edition and data.published_online:
        return data.published_online

    return data.published


def doi_datetime_get_year(doi_datetime: DoiDateTime) -> int | None:
    if doi_datetime.date_time:
        return doi_datetime.date_time.year

    if len(doi_datetime.date_parts[0]) > 0:
        return doi_datetime.date_parts[0][0]

    return None


def doi_datetime_to_string(doi_datetime: DoiDateTime) -> str:
    if doi_datetime.date_time:
        return doi_datetime.date_time.strftime('%Y-%m-%d')

    match doi_datetime.date_parts[0]:
        case [year, month, day, *_]:
            return f'{year}-{month:02}-{day:02}'

        case [year, month]:
            return f'{year}-{month:02}'

        case [year]:
            return str(year)

        case _:
            raise UnreachableException


def get_entry_type(doi_type: str) -> BibEntryType:
    match doi_type:
        case 'article' | 'journal-article':
            return 'article'

        case 'book' | 'monograph':
            return 'book'

        case 'book-chapter':
            return 'inbook'

        case _:
            return 'misc'


# We have no way of knowing whether an ISSN is digital or not, so we list them all
def get_issn(choices: list[str]) -> str | None:
    if len(choices) > 0:
        return ','.join(issn.format(sn) for sn in choices)

    return None


def get_isbn(structured: list[DoiIsbn], unstructured: list[str], *, print_edition: bool) -> str | None:
    if len(structured) == 0:
        if print_edition and len(unstructured) > 1:
            return isbn.format(unstructured[1])

        if len(unstructured) > 0:
            return isbn.format(unstructured[0])

    for choice in structured:
        if print_edition and choice.type == 'print':
            return isbn.format(choice.value)

        if not print_edition and choice.type == 'electronic':
            return isbn.format(choice.value)

    if len(structured) > 0:
        return isbn.format(structured[0].value)

    return None


def doi_data_to_bib(data: DoiData, doi: str, *, print_edition: bool = False) -> BibEntry:
    chosen_datetime = choose_doi_datetime(data, print_edition=print_edition)
    year = doi_datetime_get_year(chosen_datetime) if chosen_datetime else None
    language = normalize_language_name(data.language) if data.language else 'english'
    entry_type = get_entry_type(data.type)

    authors = list(doi_authors_to_bib(data.author))
    editors = list(doi_authors_to_bib(data.editor)) if data.editor else []

    if len(authors) == 0 and data.standards_body:
        authors.append(BibAuthor(full_name=data.standards_body.acronym))

    if isinstance(data.container_title, list):
        container_title = data.container_title[0] if len(data.container_title) > 0 else None
    else:
        container_title = data.container_title

    titles = construct_titles(
        data.title,
        data.subtitle[0] if data.subtitle and len(data.subtitle) > 0 else None
    )

    entry_name = generate_entry_name(
        authors or editors,
        str(year) if year is not None else '',
        titles,
        language,
        data.abstract,
        *(data.container_title if isinstance(data.container_title, list) else [data.container_title] if data.container_title else []),
        *(data.subtitle or []),
        *(ref.unstructured for ref in data.reference),
        *(ref.article_title for ref in data.reference),
        *(ref.journal_title for ref in data.reference),
        *(ref.volume_title for ref in data.reference),
        *(ref.series_title for ref in data.reference)
    )

    return BibEntry(
        entry_type=entry_type,
        entry_name=entry_name,
        authors=authors,
        editors=editors,
        title=titles.main,
        subtitle=titles.sub,
        publisher=data.publisher,
        language=language,
        date=doi_datetime_to_string(chosen_datetime) if chosen_datetime else None,
        doi=doi,
        pages=normalize_pages(data.page) if data.page else None,
        volume=data.volume if entry_name != 'book' else None,
        number=data.volume if entry_name == 'book' else data.article_number if entry_name == 'article' else None,
        edition=data.edition_number if data.edition_number != '1' else None,
        isbn=get_isbn(data.isbn_type, data.isbn, print_edition=print_edition),
        issn=get_issn(data.issn),
        series=container_title if entry_type == 'book' or entry_type == 'inbook' else None,
        journal=container_title if entry_type == 'article' else None,
        url=data.url if data.url != f'http://dx.doi.org/{doi}' else None
    )
