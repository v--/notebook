from collections.abc import Collection

from ...support.pytest import pytest_parametrize_kwargs
from .parsing import parse_formula
from .signature import FormalLogicSignature
from .variables import get_formula_free_variables


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',   expected={'x', 'y'}),
    dict(formula='(x = y)',   expected={'x', 'y'}),
    dict(formula='(x₁ = y₂)', expected={'x₁', 'y₂'}),
    dict(formula='p²(x, y)',  expected={'x', 'y'}),
    dict(formula='∀y.p¹(x)',  expected={'x'}),
    dict(formula='∀x.p¹(x)',  expected=set()),
    dict(
        formula='((∀y.p¹(y) ∨ q¹(x)) ∧ ∃y.r¹(y))',
        expected={'x'}
    ),
)
def test_get_open_variables(formula: str, expected: Collection[str], dummy_signature: FormalLogicSignature) -> None:
    actual = set(map(str, get_formula_free_variables(parse_formula(formula, dummy_signature))))
    assert actual == expected

