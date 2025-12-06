from ....support.pytest import pytest_parametrize_kwargs
from ..propositional import parse_propositional_formula
from .dual import DualFormulaKind, to_dual_formula


@pytest_parametrize_kwargs(
    dict(formula='⊤', expected='⊤'),
    dict(formula='p', expected='¬p'),
    dict(formula='¬p', expected='p'),
    dict(formula='(p ∨ ¬q)', expected='(¬p ∨ q)'),
    dict(formula='(p ∧ ¬q)', expected='(¬p ∧ q)'),
    dict(formula='(p → ¬q)', expected='(¬p → q)'),
    dict(formula='(p ↔ ¬q)', expected='(¬p ↔ q)'),
    dict(formula='((p ∨ ¬q) → r)', expected='((¬p ∨ q) → ¬r)'),
)
def test_to_dual_formula_literals(formula: str, expected: str) -> None:
    assert str(to_dual_formula(parse_propositional_formula(formula), DualFormulaKind.LITERALS)) == expected


@pytest_parametrize_kwargs(
    dict(formula='⊤', expected='⊥'),
    dict(formula='p', expected='p'),
    dict(formula='¬p', expected='¬p'),
    dict(formula='(p ∨ ¬q)', expected='(p ∧ ¬q)'),
    dict(formula='(p ∧ ¬q)', expected='(p ∨ ¬q)'),
    dict(formula='(p → ¬q)', expected='(¬q → p)'),
    dict(formula='(p ↔ ¬q)', expected='(p ↔ ¬q)'),
    dict(formula='((p ∨ ¬q) → r)', expected='(r → (p ∧ ¬q))'),
)
def test_to_dual_formula_connectives(formula: str, expected: str) -> None:
    assert str(to_dual_formula(parse_propositional_formula(formula), DualFormulaKind.CONNECTIVES)) == expected


@pytest_parametrize_kwargs(
    dict(formula='⊤', expected='⊥'),
    dict(formula='p', expected='¬p'),
    dict(formula='¬p', expected='p'),
    dict(formula='(p ∨ ¬q)', expected='(¬p ∧ q)'),
    dict(formula='(p ∧ ¬q)', expected='(¬p ∨ q)'),
    dict(formula='(p → ¬q)', expected='(q → ¬p)'),
    dict(formula='(p ↔ ¬q)', expected='(¬p ↔ q)'),
    dict(formula='((p ∨ ¬q) → r)', expected='(¬r → (¬p ∧ q))'),
)
def test_to_dual_formula_combined(formula: str, expected: str) -> None:
    assert str(to_dual_formula(parse_propositional_formula(formula), DualFormulaKind.COMBINED)) == expected
