import pytest

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
        '{A: B}':   Titles('{A: B}', None)
    }.items()
)
def test_split_title(string: str, expected: Titles) -> None:
    assert split_title(string) == expected
