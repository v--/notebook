from ....support.pytest import pytest_parametrize_kwargs
from .formulas import PropNegationFormula
from .parsing import parse_prop_formula
from .sat import are_equisatisfiable, are_semantically_equivalent, brute_force_satisfy, is_contradiction, is_tautology


@pytest_parametrize_kwargs(
    dict(formula='⊤'),
    dict(formula='p'),
    dict(formula='¬p'),
    dict(formula='(⊥ ∨ p)'),
    dict(formula='((p ∧ q) → (p ∨ q))'),
)
def test_brute_force_satisfy_success(formula: str) -> None:
    formula_ = parse_prop_formula(formula)
    model = brute_force_satisfy(formula_)
    assert model is not None


@pytest_parametrize_kwargs(
    dict(formula='⊥'),
    dict(formula='¬⊤'),
    dict(formula='(p ∧ ¬p)'),
)
def test_brute_force_satisfy_failure(formula: str) -> None:
    formula_ = parse_prop_formula(formula)
    model = brute_force_satisfy(formula_)
    assert model is None


@pytest_parametrize_kwargs(
    dict(formula='⊤'),
    dict(formula='(⊥ → p)'),
    dict(formula='(p ∨ ¬p)'),
    dict(formula='(p → (p → (q → p)))'),
)
def test_is_tautology(formula: str) -> None:
    formula_ = parse_prop_formula(formula)
    assert brute_force_satisfy(PropNegationFormula(formula_)) is None
    assert is_tautology(formula_)


@pytest_parametrize_kwargs(
    dict(formula='⊥'),
    dict(formula='(⊤ → ⊥)'),
    dict(formula='¬(p ∨ ¬p)'),
)
def test_is_contradiction(formula: str) -> None:
    formula_ = parse_prop_formula(formula)
    assert brute_force_satisfy(formula_) is None
    assert is_contradiction(formula_)


@pytest_parametrize_kwargs(
    dict(first='p',         second='p'),
    dict(first='p',         second='(p ∨ p)'),
    dict(first='(p ∨ q)',   second='¬(¬p ∧ ¬q)'),
    dict(first='(p → q)',   second='(¬q → ¬p)'),
)
def test_are_semantically_equivalent_success(first: str, second: str) -> None:
    first_ = parse_prop_formula(first)
    second_ = parse_prop_formula(second)
    assert are_semantically_equivalent(first_, second_)


@pytest_parametrize_kwargs(
    dict(first='p',         second='q'),
    dict(first='(p ∨ q)',   second='(p ∧ q)'),
    dict(first='(p → q)',   second='(q → p)'),
)
def test_are_semantically_equivalent_failure(first: str, second: str) -> None:
    first_ = parse_prop_formula(first)
    second_ = parse_prop_formula(second)
    assert not are_semantically_equivalent(first_, second_)


@pytest_parametrize_kwargs(
    dict(first='⊤',         second='(p ∨ ¬p)'),
    dict(first='p',         second='p'),
    dict(first='p',         second='¬p'),
    dict(first='p',         second='q'),
    dict(first='(p → q)',   second='(q → p)'),
)
def test_are_equisatisfiable_success(first: str, second: str) -> None:
    first_ = parse_prop_formula(first)
    second_ = parse_prop_formula(second)
    assert are_equisatisfiable(first_, second_)


@pytest_parametrize_kwargs(
    dict(first='⊤',         second='⊥'),
    dict(first='(p ∨ ¬p)',  second='¬(p ∨ ¬p)'),
)
def test_are_equisatisfiable_failure(first: str, second: str) -> None:
    first_ = parse_prop_formula(first)
    second_ = parse_prop_formula(second)
    assert not are_equisatisfiable(first_, second_)
