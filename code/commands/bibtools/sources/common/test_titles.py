from notebook.bibtex.parsing import parse_value
from notebook.bibtex.string import VerbatimString
from notebook.support.pytest import pytest_parametrize_kwargs

from .titles import Titles, split_title


@pytest_parametrize_kwargs(
    dict(string='A: B',    expected=Titles('A', 'B')),
    dict(string='A: B: C', expected=Titles('A', 'B: C')),
    dict(string='A. B',    expected=Titles('A', 'B')),
    dict(string='A: B. C', expected=Titles('A', 'B. C')),
    dict(string='A - B',   expected=Titles('A', 'B')),
    dict(string='A -- B',  expected=Titles('A', 'B')),
    dict(string='A --- B', expected=Titles('A', 'B')),
    dict(string='A-B C',   expected=Titles('A-B C', None)),
    dict(string='{A: B}',  expected=Titles(VerbatimString('A: B'), None))
)
def test_split_title(string: str, expected: Titles) -> None:
    assert split_title(parse_value(string)) == expected
