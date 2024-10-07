import pytest

from notebook.bibtex.parsing import parse_value
from notebook.bibtex.string import VerbatimString

from .titles import Titles, split_title


@pytest.mark.parametrize(
    ('string', 'expected'),
    {
        'A: B':    Titles('A', 'B'),
        'A: B: C': Titles('A', 'B: C'),
        'A. B':    Titles('A', 'B'),
        'A: B. C': Titles('A', 'B. C'),
        'A - B':   Titles('A', 'B'),
        'A -- B':  Titles('A', 'B'),
        'A --- B': Titles('A', 'B'),
        'A-B C':   Titles('A-B C', None),
        '{A: B}':  Titles(VerbatimString('A: B'), None)
    }.items()
)
def test_split_title(string: str, expected: Titles) -> None:
    assert split_title(parse_value(string)) == expected
