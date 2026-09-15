import re

lazy from notebook.bibtex import BibEntry

from .bib import stackexchange_post_to_bib
from .fetch import fetch_stackexchange_json
from .model import parse_stackexchange_answer_json, parse_stackexchange_question_json
from .url_parser import StackExchangeUrl


REGEX = re.compile(r'https?://(?P<url>[\w.]+)/(?P<type>[qa])/(?P<question_id>\d+)(/(?P<answer_id>\d+))?$')


def retrieve_stackexchange_entry(parsed_url: StackExchangeUrl, *, dump_as_fixture: bool) -> BibEntry:
    if parsed_url.is_answer:
        answer_json = fetch_stackexchange_json(parsed_url.site, parsed_url.post_id, is_answer=True, dump_as_fixture=dump_as_fixture)
        answers = parse_stackexchange_answer_json(answer_json)
        first_answer = answers.items[0]
        question_json = fetch_stackexchange_json(parsed_url.site, first_answer.question_id, is_answer=False, dump_as_fixture=dump_as_fixture)
    else:
        first_answer = None
        question_json = fetch_stackexchange_json(parsed_url.site, parsed_url.post_id, is_answer=False, dump_as_fixture=dump_as_fixture)

    questions = parse_stackexchange_question_json(question_json)
    first_question = questions.items[0]
    return stackexchange_post_to_bib(first_question, first_answer, parsed_url)
