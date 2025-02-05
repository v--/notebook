from notebook.support.pytest import pytest_parametrize_kwargs

from .unicode import (
    Capitalization,
    atoi_subscripts,
    is_greek_string,
    is_latin_string,
    itoa_subscripts,
    normalize_whitespace,
    remove_accents,
    remove_symbols,
    to_superscript,
)


@pytest_parametrize_kwargs(
    dict(string='abc', expected='ᵃᵇᶜ'),
    dict(string='ABC', expected='ᴬᴮꟲ'),
    dict(string='AbC', expected='ᴬᵇꟲ'),
    dict(string='абв', expected='абв'),
)
def test_to_superscript(string: str, expected: str) -> None:
    assert to_superscript(string) == expected


@pytest_parametrize_kwargs(
    dict(string='₀',     expected=0),
    dict(string='₁₂₃₄',  expected=1234),
    dict(string='₋₁₂₃₄', expected=-1234),
)
def test_atoi_subscripts(string: str, expected: int) -> None:
    assert atoi_subscripts(string) == expected


@pytest_parametrize_kwargs(
    dict(value=0,     expected='₀'),
    dict(value=1234,  expected='₁₂₃₄'),
    dict(value=-1234, expected='₋₁₂₃₄'),
)
def test_itoa_subscripts(value: int, expected: str) -> None:
    assert itoa_subscripts(value) == expected


def xnor(a: bool, b: bool) -> bool:  # noqa: FBT001
    return a == b


def test_is_latin_string_capitaliation(string: str = 'abc') -> None:
    lower = string.lower()
    upper = string.upper()
    mixed = string.title()

    for cap in Capitalization:
        assert xnor(Capitalization.lower in cap, is_latin_string(lower, capitalization=cap))
        assert xnor(Capitalization.upper in cap, is_latin_string(upper, capitalization=cap))
        assert xnor(Capitalization.mixed in cap, is_latin_string(mixed, capitalization=cap))


def test_is_greek_string_capitaliation(string: str = 'τσρ') -> None:
    lower = string.lower()
    upper = string.upper()
    mixed = string.title()

    for cap in Capitalization:
        assert xnor(Capitalization.lower in cap, is_greek_string(lower, capitalization=cap))
        assert xnor(Capitalization.upper in cap, is_greek_string(upper, capitalization=cap))
        assert xnor(Capitalization.mixed in cap, is_greek_string(mixed, capitalization=cap))


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
    dict(string='lorem',  expected='lorem'),
    dict(string='Fučík',  expected='Fučík'),
    dict(string='l_o.r!e⧦m',  expected='lorem'),
    dict(string='l o r e m',  expected='l o r e m'),
)
def test_remove_symbols(string: str, expected: str) -> None:
    assert remove_symbols(string) == expected


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
