from notebook.support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists

from .titles import title_case


@pytest_parametrize_lists(
    string=[
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


@pytest_parametrize_kwargs(
    dict(string='word',      expected='Word'),
    dict(string='word word', expected='Word Word')
)
def test_name_to_bib_author(string: str, expected: str) -> None:
    assert title_case(string) == expected
