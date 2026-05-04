from notebook.support.pytest import pytest_parametrize_kwargs

from .scripts import atoi_subscripts, itoa_subscripts, to_superscript


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
