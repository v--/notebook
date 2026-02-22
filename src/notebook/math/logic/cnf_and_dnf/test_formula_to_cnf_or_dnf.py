from ....support.pytest import pytest_parametrize_kwargs
from ..propositional import are_semantically_equivalent, parse_prop_formula
from .formula_to_cnf_or_dnf import formula_to_cnf_prop
from .validation import is_formula_in_cnf


@pytest_parametrize_kwargs(
    # Trivial cases
    dict(formula='⊤', expected='⊤'),
    dict(formula='⊥', expected='⊥'),
    dict(formula='p', expected='p'),
    dict(formula='(p ∧ q)', expected='(p ∧ q)'),
    dict(formula='(p ∨ q)', expected='(p ∨ q)'),

    # Pushing negations
    dict(formula='¬(p ∧ q)', expected='(¬p ∨ ¬q)'),
    dict(formula='¬¬(p ∧ q)', expected='(p ∧ q)'),
    dict(formula='¬(¬p ∧ ¬q)', expected='(p ∨ q)'),
    dict(formula='¬(p ∧ (q ∧ ¬r))', expected='(¬p ∨ (¬q ∨ r))'),
    dict(formula='¬(p ∧ ¬(q ∨ ¬r))', expected='(¬p ∨ (q ∨ ¬r))'),

    # Removing conditionals
    dict(formula='(p → q)',  expected='(¬p ∨ q)'),
    dict(formula='(¬p → q)', expected='(p ∨ q)'),
    dict(formula='¬(p → q)', expected='(p ∧ ¬q)'),
    dict(formula='(p ∨ (q ↔ r))', expected='((p ∨ (¬q ∨ r)) ∧ (p ∨ (q ∨ ¬r)))'),

    # Removing biconditionals
    dict(formula='(p ↔ q)',  expected='((¬p ∨ q) ∧ (p ∨ ¬q))'),
    dict(formula='(¬p ↔ q)', expected='((p ∨ q) ∧ (¬p ∨ ¬q))'),
    dict(formula='¬(p ↔ q)', expected='((¬p ∨ ¬q) ∧ (p ∨ q))'),

    # Pulling conjunctions
    dict(formula='(p ∨ (q ∧ r))', expected='((p ∨ q) ∧ (p ∨ r))'),
    dict(formula='((p ∧ q) ∨ r)', expected='((p ∨ r) ∧ (q ∨ r))'),
    dict(formula='((p ∧ q) ∨ (r ∧ s))', expected='(((p ∨ r) ∧ (p ∨ s)) ∧ ((q ∨ r) ∧ (q ∨ s)))'),
    dict(formula='(p ∨ (q → (r ∧ s)))', expected='((p ∨ (¬q ∨ r)) ∧ (p ∨ (¬q ∨ s)))'),
    dict(formula='(p ∧ ¬(q → r))', expected='(p ∧ (q ∧ ¬r))'),
    dict(
        formula='(p ∨ (q ∨ (r ∨ (s ∧ t))))',
        expected='((p ∨ (q ∨ (r ∨ s))) ∧ (p ∨ (q ∨ (r ∨ t))))'
    ),
    dict(formula='¬(p ∧ (q ∨ r))', expected='((¬p ∨ ¬q) ∧ (¬p ∨ ¬r))'), # We distribute the dual of the inner formula
)
def test_formula_to_cnf_prop(formula: str, expected: str) -> None:
    formula_ = parse_prop_formula(formula)
    expected_ = parse_prop_formula(expected)

    assert is_formula_in_cnf(expected_)
    assert are_semantically_equivalent(formula_, expected_)

    result = formula_to_cnf_prop(formula_)
    assert result == expected_
