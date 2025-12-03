from datetime import datetime

import pytest

from .....bibtex.author import BibAuthor
from .....bibtex.entry import BibEntry
from .....bibtex.string import VerbatimString
from ...exceptions import BibToolsParsingError
from ..common.dates import to_iso_date
from .bib import stackexchange_entry_to_bib
from .fixtures import get_stackexchange_fixture_path
from .model import parse_stackexchange_html


TODAY = to_iso_date(datetime.now())


def test_parse_invalid(identifier: str = 'invalid') -> None:
    with get_stackexchange_fixture_path(identifier).open() as file:
        html = file.read()

    with pytest.raises(BibToolsParsingError):
        parse_stackexchange_html(html)


def test_parse_mathse_question_4272953_229174(identifier: str = 'https://math.stackexchange.com/q/4272953/229174') -> None:
    with get_stackexchange_fixture_path(identifier).open() as file:
        html = file.read()

    res = parse_stackexchange_html(html)
    entry = stackexchange_entry_to_bib(res, identifier)
    assert entry == BibEntry(
        entry_type='online',
        entry_name='MathSE:how_do_you_extend_the_topological_semantics_for_intuitionistic_propositional_logic_ipc_to_a_semantics_for_intuitionistic_first_order_logic_ifol',
        title='How do you extend the topological semantics for intuitionistic propositional logic (IPC) to a semantics for intuitionistic first order logic (IFOL)?',
        authors=[BibAuthor(full_name='Greg Nisbet')],
        languages=['english'],
        addendum='Citation of question',
        date='2021-10-10',
        titleaddon='Mathematics Stack Exchange',
        url=identifier,
        urldate=TODAY
    )


def test_parse_mathof_answer_231571(identifier: str='https://mathoverflow.net/a/231571') -> None:
    with get_stackexchange_fixture_path(identifier).open() as file:
        html = file.read()

    res = parse_stackexchange_html(html)
    entry = stackexchange_entry_to_bib(res, identifier)
    assert entry == BibEntry(
        entry_type='online',
        entry_name='MathOS:functions_of_several_variables_over_finite_fields',
        title='Functions of several variables over finite fields',
        authors=[BibAuthor(full_name=VerbatimString("User ``user9072''"))],
        languages=['english'],
        addendum='Citation of answer',
        date='2016-02-19',
        titleaddon='MathOverflow',
        url=identifier,
        urldate=TODAY
    )
