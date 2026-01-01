from ....support.pytest import pytest_parametrize_kwargs
from ..propositional import are_semantically_equivalent, parse_prop_formula
from .collapse_constants import collapse_constants_prop


@pytest_parametrize_kwargs(
    dict(formula='p', expected=None),
    dict(formula='⊤', expected=None),

    # Conjunction
    dict(formula='(p ∧ ⊤)', expected='p'),
    dict(formula='(p ∧ ⊥)', expected='⊥'),
    dict(formula='(⊤ ∧ p)', expected='p'),
    dict(formula='(⊥ ∧ p)', expected='⊥'),

    # Disjunction
    dict(formula='(p ∨ ⊤)', expected='⊤'),
    dict(formula='(p ∨ ⊥)', expected='p'),
    dict(formula='(⊤ ∨ p)', expected='⊤'),
    dict(formula='(⊥ ∨ p)', expected='p'),

    # Implication
    dict(formula='(p → ⊤)', expected='⊤'),
    dict(formula='(p → ⊥)', expected='¬p'),
    dict(formula='(⊤ → p)', expected='p'),
    dict(formula='(⊥ → p)', expected='⊤'),

    # Equivalence
    dict(formula='(⊤ ↔ ⊤)', expected='⊤'),
    dict(formula='(⊥ ↔ ⊥)', expected='⊤'),
    dict(formula='(⊤ ↔ ⊥)', expected='⊥'),
    dict(formula='(⊥ ↔ ⊤)', expected='⊥'),

    dict(formula='(p ↔ ⊤)', expected=None),
    dict(formula='(p ↔ ⊥)', expected=None),
    dict(formula='(⊤ ↔ p)', expected=None),
    dict(formula='(⊥ ↔ p)', expected=None),
)
def test_collapse(formula: str, expected: str | None) -> None:
    formula_ = parse_prop_formula(formula)
    expected_ = formula_ if expected is None else parse_prop_formula(expected)
    assert are_semantically_equivalent(formula_, expected_)

    result = collapse_constants_prop(formula_)
    assert result == expected_
