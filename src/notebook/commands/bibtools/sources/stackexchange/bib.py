import html
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
lazy from collections.abc import Iterable

from notebook.bibtex import BibAuthor, BibEntry, BibString, VerbatimString
from notebook.commands.bibtools.exceptions import BibToolsDecodingError
from notebook.commands.bibtools.sources.helpers.dates import to_iso_date
from notebook.support.iteration import string_accumulator

from .model import StackExchangeAnswer, StackExchangeQuestion
from .url_parser import StackExchangeUrl


@dataclass(frozen=True)
class SeSiteName:
    slug: str
    full: str


SITE_NAME_MAP = {
    'codegolf.stackexchange.com': SeSiteName('CGSE', 'Code Golf Stack Exchange'),
    'hsm.stackexchange.com': SeSiteName('HSMSE', 'History of Science and Mathematics Stack Exchange'),
    'mathoverflow.net': SeSiteName('MathOF', 'MathOverflow'),
    'math.stackexchange.com': SeSiteName('MathSE', 'Math Stack Exchange'),
    'softwareengineering.stackexchange.com': SeSiteName('SESE', 'Software Engineering Stack Exchange'),
    'stackoverflow.com': SeSiteName('SE', 'StackOverflow'),
    'cstheory.stackexchange.com': SeSiteName('TCSSE', 'Theoretical Computer Science Stack Exchange'),
}


@string_accumulator()
def mangle_title(title: str) -> Iterable[str]:
    for char in unicodedata.normalize('NFKD', title):
        category = unicodedata.category(char)

        if category.startswith('L'):
            yield char.lower()

        if category.startswith('Z'):
            yield '_'


def stackexchange_post_to_bib(question: StackExchangeQuestion, answer: StackExchangeAnswer | None, parsed_url: StackExchangeUrl) -> BibEntry:
    if parsed_url.site not in SITE_NAME_MAP:
        raise BibToolsDecodingError(f'Cannot generate an entry name for {parsed_url.site!r} because we do not have a dedicated prefix.')

    post = answer or question
    author_name: BibString = post.owner.display_name if len(post.owner.display_name.split()) > 1 else VerbatimString(f"User ``{post.owner.display_name}''")
    title = html.unescape(question.title)

    return BibEntry(
        entry_type='online',
        entry_name=SITE_NAME_MAP[parsed_url.site].slug + ':' + mangle_title(title),
        authors=[BibAuthor(author_name)],
        title=title,
        titleaddon=SITE_NAME_MAP[parsed_url.site].full,
        languages=['english'],
        urldate=to_iso_date(datetime.now(tz=UTC)),
        date=to_iso_date(datetime.fromtimestamp(post.creation_date, tz=UTC)),
        url=parsed_url.raw,
        addendum='Citation of question' if answer is None else 'Citation of answer',
    )
