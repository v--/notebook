from ....support.pytest import pytest_parametrize_kwargs
from ..propositional import (
    are_semantically_equivalent,
    parse_prop_formula,
)
from .collapse_repeated_negation import collapse_repeated_negation_prop


@pytest_parametrize_kwargs(
    dict(formula='⊤',         collapsed='⊤'),
    dict(formula='¬⊤',        collapsed='¬⊤'),
    dict(formula='¬¬⊤',       collapsed='⊤'),
    dict(formula='¬¬¬⊤',      collapsed='¬⊤'),
    dict(formula='p',         collapsed='p'),
    dict(formula='¬p',        collapsed='¬p'),
    dict(formula='¬¬p',       collapsed='p'),
    dict(formula='¬¬¬p',      collapsed='¬p'),
    dict(
        formula='((p ∨ ¬¬p) ∧ q)',
        collapsed='((p ∨ p) ∧ q)',
    ),
    dict(
        formula='¬¬¬(¬¬p ∧ ¬q)',
        collapsed='¬(p ∧ ¬q)'
    ),
)
def test_collapse_repeated_negation_prop(formula: str, collapsed: str) -> None:
    formula_ = parse_prop_formula(formula)
    collapsed_ = parse_prop_formula(collapsed)

    are_semantically_equivalent(formula_, collapsed_)

    result = collapse_repeated_negation_prop(formula_)
    assert result == collapsed_
