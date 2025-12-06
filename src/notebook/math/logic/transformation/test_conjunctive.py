from collections.abc import Callable

from ....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..propositional import parse_propositional_formula
from .conjunctive import formula_to_cnf, function_to_cnf, is_formula_in_cnf, pull_conjunction


@pytest_parametrize_lists(
    formula=[
        'p',
        '(p ∧ q)',
        '(p ∧ (q ∨ r))',
    ]
)
def test_is_formula_in_cnf_success(formula: str) -> None:
    assert is_formula_in_cnf(parse_propositional_formula(formula))


@pytest_parametrize_lists(
    formula=[
        '(p → q)',
        '(p ∨ (q ∧ r))',
    ]
)
def test_is_formula_in_cnf_failure(formula: str) -> None:
    assert not is_formula_in_cnf(parse_propositional_formula(formula))


@pytest_parametrize_kwargs(
    # Trivial cases
    dict(formula='p', expected='p'),
    dict(formula='(p ∧ q)', expected='(p ∧ q)'),
    dict(formula='(p ∨ q)', expected='(p ∨ q)'),

    # Base cases
    dict(formula='(p ∨ (q ∧ r))', expected='((p ∨ q) ∧ (p ∨ r))'),
    dict(formula='((p ∧ q) ∨ r)', expected='((p ∨ r) ∧ (q ∨ r))'),

    # Test pulling out nested conjunctions
    dict(formula='((p ∧ q) ∨ (r ∧ s))', expected='(((p ∨ r) ∧ (p ∨ s)) ∧ ((q ∨ r) ∧ (q ∨ s)))'),
    dict(formula='(p ∧ (q ∨ (r ∧ s)))', expected='(p ∧ ((q ∨ r) ∧ (q ∨ s)))'),
    dict(formula='(p ∨ (q ∨ (r ∧ s)))', expected='((p ∨ (q ∨ r)) ∧ (p ∨ (q ∨ s)))'),
    dict(formula='(p ∨ (q ∧ (r ∧ s)))', expected='((p ∨ q) ∧ ((p ∨ r) ∧ (p ∨ s)))'),
    dict(
        formula='(p ∨ (q ∨ (r ∨ (s ∧ t))))',
        expected='((p ∨ (q ∨ (r ∨ s))) ∧ (p ∨ (q ∨ (r ∨ t))))'
    ),

    # Other connectives are allowed, but we will stop once we reach them
    dict(
        formula='(p ∨ (q → (r ∧ s)))',
        expected='(p ∨ (q → (r ∧ s)))'
    ),
)
def test_pull_conjunction(formula: str, expected: str) -> None:
    assert str(pull_conjunction(parse_propositional_formula(formula))) == expected


@pytest_parametrize_kwargs(
    dict(formula='p', expected='p'),

    dict(formula='⊤', expected='(p ∨ ¬p)'),
    dict(formula='⊥', expected='(p ∧ ¬p)'),

    dict(formula='(p ∨ q)', expected='(p ∨ q)'),
    dict(formula='(p ∧ q)', expected='(p ∧ q)'),
    dict(formula='(p → q)', expected='(¬p ∨ q)'),
    dict(formula='(p ↔ q)', expected='((¬p ∨ q) ∧ (p ∨ ¬q))'),

    dict(formula='¬(p ∧ q)', expected='(¬p ∨ ¬q)'),
    dict(formula='¬(p ∨ q)', expected='(¬p ∧ ¬q)'),
    dict(formula='¬(p → q)', expected='(p ∧ ¬q)'),

    dict(formula='(p ∧ (q ∨ r))',   expected='(p ∧ (q ∨ r))'),
    dict(formula='¬(p ∨ ¬(q ∨ r))', expected='(¬p ∧ (q ∨ r))'),
    dict(formula='¬(p ∧ ¬(q ∧ r))', expected='((¬p ∨ q) ∧ (¬p ∨ r))'),

    dict(
        formula='(p ∨ ¬(p ∧ ¬(q ∧ r)))',
        expected='((p ∨ (¬p ∨ q)) ∧ (p ∨ (¬p ∨ r)))'
    ),
)
def test_formula_to_cnf(formula: str, expected: str) -> None:
    cnf = formula_to_cnf(parse_propositional_formula(formula))
    assert is_formula_in_cnf(cnf)
    assert str(cnf) == expected


@pytest_parametrize_kwargs(
    dict(
        predicate=lambda: True,
        expected='(p ∨ ¬p)'
    ),
    dict(
        predicate=lambda: False,
        expected='(p ∧ ¬p)'
    ),
    dict(
        predicate=lambda p, q: True,  # noqa: ARG005
        expected='(p ∨ ¬p)'
    ),
    dict(
        predicate=lambda p, q: p or q,
        expected='(p ∨ q)'
    ),
    dict(
        predicate=lambda p, q: p,  # noqa: ARG005
        expected='((p ∨ q) ∧ (p ∨ ¬q))'
    ),
    dict(
        predicate=lambda p, q: p and q,
        expected='(((p ∨ q) ∧ (p ∨ ¬q)) ∧ (¬p ∨ q))'
    ),
    dict(
        predicate=lambda p, q: False,  # noqa: ARG005
        expected='((((p ∨ q) ∧ (p ∨ ¬q)) ∧ (¬p ∨ q)) ∧ (¬p ∨ ¬q))'
    ),
)
def test_function_to_cnf(predicate: Callable[..., bool], expected: str) -> None:
    assert str(function_to_cnf(predicate)) == expected
