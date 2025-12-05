import unicodedata
from collections.abc import Iterable
from datetime import datetime

from .....bibtex import BibAuthor, BibEntry, BibString, VerbatimString
from .....support.iteration import string_accumulator
from ...exceptions import BibToolsParsingError
from ..common.dates import to_iso_date
from .model import StackExchangeEntry


SITE_ENTRY_PREFIX_MAP = {
    'Code Golf Stack Exchange': 'CGSE',
    'History of Science and Mathematics Stack Exchange': 'HSMSE',
    'MathOverflow': 'MathOS',
    'Mathematics Stack Exchange': 'MathSE',
    'Software Engineering Stack Exchange': 'SESE',
    'StackOverflow': 'SE',
    'Theoretical Computer Science Stack Exchange': 'TCSSE',
}


@string_accumulator()
def mangle_title(title: str) -> Iterable[str]:
    for char in unicodedata.normalize('NFKD', title):
        category = unicodedata.category(char)

        if category.startswith('L'):
            yield char.lower()

        if category.startswith('Z'):
            yield '_'


def stackexchange_entry_to_bib(entry: StackExchangeEntry, identifier: str) -> BibEntry:
    if entry.site not in SITE_ENTRY_PREFIX_MAP:
        raise BibToolsParsingError(f'Cannot generate an entry name for {entry.site!r} because we do not have a dedicated prefix.')

    author_name: BibString = entry.author_username if len(entry.author_username.split()) > 1 else VerbatimString(f"User ``{entry.author_username}''")

    return BibEntry(
        entry_type='online',
        entry_name=SITE_ENTRY_PREFIX_MAP[entry.site] + ':' + mangle_title(entry.title),
        authors=[BibAuthor(author_name)],
        title=entry.title,
        titleaddon=entry.site,
        languages=['english'],
        urldate=to_iso_date(datetime.now()),
        date=to_iso_date(entry.datetime),
        url=identifier,
        addendum='Citation of question' if entry.answer_id is None else 'Citation of answer'
    )
