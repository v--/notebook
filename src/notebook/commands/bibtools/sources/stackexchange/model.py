import json
import re
from datetime import datetime

import bs4
from pydantic import BaseModel

from ...exceptions import BibToolsParsingError


class StackExchangeEntry(BaseModel):
    title: str
    site: str
    author_username: str
    datetime: datetime
    question_id: str
    answer_id: str | None


def get_tag_attribute(tag: bs4.Tag, attribute_name: str) -> str:
    attribute = tag[attribute_name]

    if not isinstance(attribute, str):
        raise BibToolsParsingError(f'Unsupported tag value {attribute!r}')

    return attribute


def parse_stackexchange_html(html: str) -> StackExchangeEntry:
    soup = bs4.BeautifulSoup(html, 'html.parser')
    title_tag = soup.find('meta', property='og:title')

    if not isinstance(title_tag, bs4.Tag):
        raise BibToolsParsingError('No title element found')

    site_tag = soup.find('meta', property='og:site_name')

    if not isinstance(site_tag, bs4.Tag):
        raise BibToolsParsingError('No site tag found')

    signup_json_tag = soup.find('script', **{'data-module-name': 'islands/signup-modal/index.mod'})  # type: ignore[arg-type]

    if not isinstance(signup_json_tag, bs4.Tag):
        raise BibToolsParsingError('No signup metainformation tag found')

    signup_json = json.loads(signup_json_tag.text)
    full_url = signup_json['ReturnUrl']
    match = re.match(r'https://[\w.]+/questions/(?P<question_id>\d+)/[\w\-]+(/(?P<answer_id>\d+))?', full_url)

    if match is None:
        raise BibToolsParsingError(f'Could not parse full URL {full_url}')

    if match is None:
        raise BibToolsParsingError(f'Could not parse full URL {full_url}')

    question_id = match.group('question_id')
    answer_id = match.group('answer_id')

    if answer_id is None:
        question_container = soup.find(**{'data-questionid': question_id})  # type: ignore[arg-type]

        if not isinstance(question_container, bs4.Tag):
            raise BibToolsParsingError(f'No question container found for id {question_id}')

        author_username = get_tag_attribute(question_container, 'data-author-username')
        datetime_tag = question_container.find('span', 'relativetime')

        if not isinstance(datetime_tag, bs4.Tag):
            raise BibToolsParsingError('No datetime tag found')

        datetime_str = get_tag_attribute(datetime_tag, 'title')
        datetime_ = datetime.fromisoformat(datetime_str)
    else:
        answer_container = soup.find(**{'data-answerid': answer_id})  # type: ignore[arg-type]

        if not isinstance(answer_container, bs4.Tag):
            raise BibToolsParsingError(f'No answer container found for id {answer_id}')

        author_username = get_tag_attribute(answer_container, 'data-author-username')
        datetime_tag = answer_container.find('time', itemprop='dateCreated')

        if not isinstance(datetime_tag, bs4.Tag):
            raise BibToolsParsingError('No datetime tag found')

        datetime_str = get_tag_attribute(datetime_tag, 'datetime')
        datetime_ = datetime.fromisoformat(datetime_str)

    return StackExchangeEntry(
        title=get_tag_attribute(title_tag, 'content'),
        site=get_tag_attribute(site_tag, 'content'),
        author_username=author_username,
        datetime=datetime_,
        question_id=question_id,
        answer_id=answer_id,
    )
