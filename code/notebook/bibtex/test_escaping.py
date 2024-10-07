from ..support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from .escaping import escape


@pytest_parametrize_lists(
    string=[
        '',
        'test',
        'test test',
        '\\\\',
        '\\&'
    ]
)
def test_escape_noop(string: str) -> None:
    assert string == escape(string)


@pytest_parametrize_kwargs(
    dict(string='&',           expected='\\&'),
    dict(string='@',           expected='\\@'),
    dict(string='test & test', expected='test \\& test')
)
def test_escape(string: str, expected: str) -> None:
    assert escape(string) == expected
