from .....support.pytest import pytest_parametrize_lists
from ...propositional import parse_prop_formula
from .validation import is_formula_in_cnf


@pytest_parametrize_lists(
    formula=[
        '⊤',
        'p',
        '(p ∧ q)',
        '(p ∧ (q ∨ r))',
    ]
)
def test_is_formula_in_cnf_success(formula: str) -> None:
    formula_ = parse_prop_formula(formula)
    assert is_formula_in_cnf(formula_)


@pytest_parametrize_lists(
    formula=[
        '(p → q)',
        '(p ∨ (q ∧ r))',
    ]
)
def test_is_formula_in_cnf_failure(formula: str) -> None:
    formula_ = parse_prop_formula(formula)
    assert not is_formula_in_cnf(formula_)
