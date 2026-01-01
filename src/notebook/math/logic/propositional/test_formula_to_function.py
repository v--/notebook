from collections.abc import Callable

from ....support.pytest import pytest_parametrize_kwargs
from .formula_to_function import prop_formula_to_function
from .parsing import parse_prop_formula
from .sat import iter_interpretations


@pytest_parametrize_kwargs(
    dict(
        formula='⊤',
        function=lambda: True,
    ),

    dict(
        formula='⊥',
        function=lambda: False,
    ),

    dict(
        formula='p',
        function=lambda p: p,
    ),

    dict(
        formula='¬p',
        function=lambda p: not p,
    ),

    dict(
        formula='(p ∧ q)',
        function=lambda p, q: p and q,
    ),

    dict(
        formula='(q ∧ p)', # Verify that the inferred order of the variables is alphabetic
        function=lambda p, q: p and q,
    ),

    dict(
        formula='(p ∨ q)',
        function=lambda p, q: p or q,
    ),

    dict(
        formula='(p → q)',
        function=lambda p, q: not p or q,
    ),

    dict(
        formula='(p ↔ q)',
        function=lambda p, q: p == q,
    ),

    dict(
        formula='(p ↔ q)',
        function=lambda p, q: p == q,
    ),

    dict(
        formula='¬(p ↔ q)',
        function=lambda p, q: p != q,
    ),
)
def test_prop_formula_to_function(formula: str, function: Callable[..., bool]) -> None:
    formula_ = parse_prop_formula(formula)
    result = prop_formula_to_function(formula_)

    for interp in iter_interpretations(formula_):
        kwargs = {var.symbol.name: value for var, value in interp.mapping.items()}
        assert function(**kwargs) == result(**kwargs)
