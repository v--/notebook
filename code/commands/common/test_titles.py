import pytest

from .titles import title_case


@pytest.mark.parametrize(
    'string',
    [
        '',
        'Word',
        'Word Word',
        'Word  Word',
        'WORD',
        'слово'
    ]
)
def test_name_to_bib_author_noop(string: str) -> None:
    assert title_case(string) == string


@pytest.mark.parametrize(
    ('string', 'expected'),
    {
        'word': 'Word',
        'word word': 'Word Word',
    }.items()
)
def test_name_to_bib_author(string: str, expected: str) -> None:
    assert title_case(string) == expected
