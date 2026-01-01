from ....support.pytest import pytest_parametrize_kwargs
from .parsing import parse_prop_formula
from .substitute_subformula import substitute_subformula


@pytest_parametrize_kwargs(
    dict(formula='⊤',        src='⊤',  dest='⊥', expected='⊥'),
    dict(formula='(p ∨ q)',  src='p',  dest='⊥', expected='(⊥ ∨ q)'),
    dict(formula='(¬p ∨ q)', src='¬p', dest='⊥', expected='(⊥ ∨ q)'),
)
def test_substitute_in_formula(formula: str, src: str, dest: str, expected: str) -> None:
    formula_ = parse_prop_formula(formula)
    expected_ = parse_prop_formula(expected)
    result = substitute_subformula(
        formula_,
        parse_prop_formula(src),
        parse_prop_formula(dest),
    )

    assert result == expected_
