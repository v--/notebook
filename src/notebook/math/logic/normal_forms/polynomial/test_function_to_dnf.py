from collections.abc import Callable

from .....support.pytest import pytest_parametrize_kwargs
from ...propositional import parse_prop_formula
from .function_to_dnf import function_to_dnf
from .validation import is_formula_in_dnf


@pytest_parametrize_kwargs(
    # Canonically true
    dict(
        function=lambda: True,
        formula='⊤'
    ),
    dict(
        function=lambda p: True,  # noqa: ARG005
        formula='(p ∨ ¬p)'
    ),
    dict(
        function=lambda p, q: True,  # noqa: ARG005
        formula='((p ∧ q) ∨ ((p ∧ ¬q) ∨ ((¬p ∧ q) ∨ (¬p ∧ ¬q))))'
    ),

    # Canonically false
    dict(
        function=lambda: False,
        formula='⊥'
    ),
    dict(
        function=lambda p: False,  # noqa: ARG005
        formula='⊥'
    ),
    dict(
        function=lambda p, q: False,  # noqa: ARG005
        formula='⊥'
    ),

    # Nonconstant unary
    dict(
        function=lambda p: p,
        formula='p'
    ),
    dict(
        function=lambda p: not p,
        formula='¬p'
    ),

    # Nonconstant binary
    dict(
        function=lambda p, q: p and q,
        formula='(p ∧ q)'
    ),
    dict(
        function=lambda p, q: p or q,
        formula='((p ∧ q) ∨ ((p ∧ ¬q) ∨ (¬p ∧ q)))'
    ),
    dict(
        function=lambda p, q: p == q,
        formula='((p ∧ q) ∨ (¬p ∧ ¬q))'
    ),

    # Nonconstant ternary
    dict(
        function=lambda p, q, r: q if p else r,
        formula='((p ∧ (q ∧ r)) ∨ ((p ∧ (q ∧ ¬r)) ∨ ((¬p ∧ (q ∧ r)) ∨ (¬p ∧ (¬q ∧ r)))))'
    ),
)
def test_function_to_dnf(function: Callable[..., bool], formula: str) -> None:
    formula_ = parse_prop_formula(formula)
    assert is_formula_in_dnf(formula_)

    result = function_to_dnf(function)
    assert result == formula_
