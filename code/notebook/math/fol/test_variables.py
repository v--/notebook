from collections.abc import Collection

from ...support.pytest import pytest_parametrize_kwargs
from .parsing import parse_formula
from .signature import FOLSignature
from .variables import get_free_variables


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',   expected={'x', 'y'}),
    dict(formula='(x = y)',   expected={'x', 'y'}),
    dict(formula='(x₁ = y₂)', expected={'x₁', 'y₂'}),
    dict(formula='p₂(x, y)',  expected={'x', 'y'}),
    dict(formula='∀y.p₁(x)',  expected={'x'}),
    dict(formula='∀x.p₁(x)',  expected=set()),
    dict(
        formula='((∀y.p₁(y) ∨ q₁(x)) ∧ ∃y.r₁(y))',
        expected={'x'}
    ),
)
def test_get_free_variables(formula: str, expected: Collection[str], dummy_signature: FOLSignature) -> None:
    actual = set(map(str, get_free_variables(parse_formula(dummy_signature, formula))))
    assert actual == expected

