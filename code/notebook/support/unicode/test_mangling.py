from ..pytest import pytest_parametrize_kwargs
from .mangling import normalize_whitespace, remove_accents


@pytest_parametrize_kwargs(
    dict(string='lorem',  expected='lorem'),
    dict(string='Йордан', expected='Йордан'),
    dict(string='Fučík',  expected='Fucik'),
    dict(string='Marián', expected='Marian'),
    dict(string='Łukasz', expected='Lukasz'),
)
def test_remove_accents(string: str, expected: str) -> None:
    assert remove_accents(string) == expected


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
