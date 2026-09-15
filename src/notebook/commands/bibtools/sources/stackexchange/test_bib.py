from datetime import UTC, datetime

from notebook.bibtex import BibAuthor, BibEntry
from notebook.commands.bibtools.sources.helpers.dates import to_iso_date
from notebook.commands.bibtools.sources.stackexchange.url_parser import parse_stackexchange_url

from .bib import stackexchange_post_to_bib
from .fixtures import get_stackexchange_fixture_path
from .model import parse_stackexchange_answer_json, parse_stackexchange_question_json


TODAY = to_iso_date(datetime.now(tz=UTC))


def test_parse_mathof_question_115699(url: str = 'https://mathoverflow.net/q/115699') -> None:
    parsed_url = parse_stackexchange_url(url)
    question_json = get_stackexchange_fixture_path(parsed_url.site, parsed_url.post_id, is_answer=False).read_text()
    questions = parse_stackexchange_question_json(question_json)
    entry = stackexchange_post_to_bib(question=questions.items[0], answer=None, parsed_url=parsed_url)

    assert entry == BibEntry(
        entry_type='online',
        entry_name='MathOF:which_term_is_better_for_the_so_called_sphere_packing',
        title='Which term is better for the so called "sphere packing"?',
        authors=[BibAuthor(full_name='Hao Chen')],
        languages=['english'],
        addendum='Citation of question',
        date='2012-12-07',
        titleaddon='MathOverflow',
        url=url,
        urldate=TODAY,
    )


def test_parse_mathse_answer_2167659(url: str = 'https://math.stackexchange.com/a/2167659/229174') -> None:
    parsed_url = parse_stackexchange_url(url)
    answer_json = get_stackexchange_fixture_path(parsed_url.site, parsed_url.post_id, is_answer=True).read_text()
    answers = parse_stackexchange_answer_json(answer_json)
    question_json = get_stackexchange_fixture_path(parsed_url.site, answers.items[0].question_id, is_answer=False).read_text()
    questions = parse_stackexchange_question_json(question_json)
    entry = stackexchange_post_to_bib(question=questions.items[0], answer=answers.items[0], parsed_url=parsed_url)

    assert entry == BibEntry(
        entry_type='online',
        entry_name='MathSE:natural_categories_where_monomorphisms_differ_from_injective_morphisms',
        title='"Natural" categories where monomorphisms differ from injective morphisms',
        authors=[BibAuthor(full_name='Qiaochu Yuan')],
        languages=['english'],
        addendum='Citation of answer',
        date='2017-03-01',
        titleaddon='Math Stack Exchange',
        url=url,
        urldate=TODAY,
    )
