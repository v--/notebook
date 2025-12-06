from ....support.pytest import pytest_parametrize_kwargs
from ..propositional import are_semantically_equivalent, parse_propositional_formula
from .constants import collapse_constants, expand_constants


@pytest_parametrize_kwargs(
    dict(formula='p', expected='p'),
    dict(formula='⊤', expected='(p → p)'),
    dict(formula='⊥', expected='(p ∧ ¬p)'),
    dict(formula='(p → ⊤)', expected='(p → (p → p))'),
    dict(formula='(q → ⊤)', expected='(q → (q → q))'),
)
def test_expand_constants(formula: str, expected: str) -> None:
    formula_ = parse_propositional_formula(formula)
    expected_ = parse_propositional_formula(expected)
    assert are_semantically_equivalent(formula_, expected_)

    expanded = expand_constants(formula_)
    assert expanded == expected_


@pytest_parametrize_kwargs(
    dict(formula='p', expected='p'),
    dict(formula='⊤', expected='⊤'),

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

    dict(formula='(p ↔ ⊤)', expected='(p ↔ ⊤)'),
    dict(formula='(p ↔ ⊥)', expected='(p ↔ ⊥)'),
    dict(formula='(⊤ ↔ p)', expected='(⊤ ↔ p)'),
    dict(formula='(⊥ ↔ p)', expected='(⊥ ↔ p)'),
)
def test_eliminate_constants(formula: str, expected: str) -> None:
    formula_ = parse_propositional_formula(formula)
    expected_ = parse_propositional_formula(expected)
    assert are_semantically_equivalent(formula_, expected_)

    expanded = collapse_constants(formula_)
    assert expanded == expected_
