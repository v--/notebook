from ..pytest import pytest_parametrize_kwargs
from .whitespace import normalize_whitespace


@pytest_parametrize_kwargs(
    dict(string='a b c',  expected='a b c'),
    dict(string='a  b c', expected='a b c'),
    dict(string='a\tb c', expected='a b c'),
    dict(string='a\nb c', expected='a b c'),
    dict(string='\na b c', expected='a b c'),
    dict(string='a b c\n', expected='a b c'),
)
def test_normalize_whitespace(string: str, expected: str) -> None:
    assert normalize_whitespace(string) == expected
