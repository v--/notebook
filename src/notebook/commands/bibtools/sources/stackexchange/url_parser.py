import re
from dataclasses import dataclass

from notebook.commands.bibtools.exceptions import BibToolsParsingError


SHORT_URL_REGEX = re.compile(r'https?://(?P<site>[\w.]+)/(?P<type>[qa])/(?P<post_id>\d+)')
FULL_URL_REGEX = re.compile(r'https?://(?P<site>[\w.]+)/questions/(?P<question_id>\d+)/[^/]+(/(?P<answer_id>\d+))?')


@dataclass(frozen=True)
class StackExchangeUrl:
    raw: str
    site: str
    is_answer: bool
    post_id: int


def parse_stackexchange_url(url: str) -> StackExchangeUrl:
    if m := SHORT_URL_REGEX.match(url):
        groups = m.groupdict()

        return StackExchangeUrl(
            raw=url,
            site=groups['site'],
            is_answer=groups['type'] == 'a',
            post_id=int(groups['post_id']),
        )

    if m := FULL_URL_REGEX.match(url):
        groups = m.groupdict()

        return StackExchangeUrl(
            raw=url,
            site=groups['site'],
            is_answer=groups['answer_id'] is not None,
            post_id=int(groups['answer_id'] or groups['question_id']),
        )

    raise BibToolsParsingError(f'Could not parse URL {url}')
