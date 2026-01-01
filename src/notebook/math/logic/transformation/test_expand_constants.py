from ....support.pytest import pytest_parametrize_kwargs
from ..propositional import are_semantically_equivalent, parse_prop_formula
from .expand_constants import expand_constants_prop


@pytest_parametrize_kwargs(
    dict(formula='p', expected='p'),
    dict(formula='⊤', expected='(p → p)'),
    dict(formula='⊥', expected='(p ∧ ¬p)'),
    dict(formula='(p → ⊤)', expected='(p → (p → p))'),
    dict(formula='(q → ⊤)', expected='(q → (q → q))'),
)
def test_expand_constants(formula: str, expected: str) -> None:
    formula_ = parse_prop_formula(formula)
    expected_ = parse_prop_formula(expected)
    assert are_semantically_equivalent(formula_, expected_)

    result = expand_constants_prop(formula_)
    assert result == expected_

