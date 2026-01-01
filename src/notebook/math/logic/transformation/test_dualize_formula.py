from ....support.pytest import pytest_parametrize_kwargs
from ..parsing import parse_formula
from ..propositional import (
    evaluate_prop_formula,
    iter_interpretations,
    parse_prop_formula,
)
from ..signature import FormalLogicSignature
from .dualize_formula import dualize_formula, dualize_formula_prop


@pytest_parametrize_kwargs(
    dict(formula='⊤',         dual='⊥'),
    dict(formula='¬⊤',        dual='⊤'),
    dict(formula='¬¬⊤',       dual='⊥'),
    dict(formula='¬¬¬⊤',      dual='⊤'),
    dict(formula='p',         dual='¬p'),
    dict(formula='¬p',        dual='p'),
    dict(formula='¬¬p',       dual='¬p'),
    dict(formula='(p ∨ q)',   dual='(¬p ∧ ¬q)'),
    dict(formula='(p ∧ q)',   dual='(¬p ∨ ¬q)'),
    dict(formula='(p → q)',   dual='¬(¬q → ¬p)'),
    dict(formula='(p ↔ q)',   dual='¬(¬p ↔ ¬q)'),
    dict(formula='¬(p ∨ q)',  dual='¬(¬p ∧ ¬q)'),
    dict(formula='¬(p ∧ q)',  dual='¬(¬p ∨ ¬q)'),
    dict(formula='¬(p → q)',  dual='(¬q → ¬p)'),
    dict(formula='¬(p ↔ q)',  dual='(¬p ↔ ¬q)'),
    dict(formula='¬¬(p ∨ q)', dual='(¬p ∧ ¬q)'),
    dict(formula='¬¬(p ∧ q)', dual='(¬p ∨ ¬q)'),
    dict(formula='¬¬(p → q)', dual='¬(¬q → ¬p)'),
    dict(formula='¬¬(p ↔ q)', dual='¬(¬p ↔ ¬q)'),
    dict(
        formula='((p ∧ q) → (r ∨ s))',
        dual='¬((¬r ∧ ¬s) → (¬p ∨ ¬q))'
    ),
)
def test_dualize_formula_prop(formula: str, dual: str) -> None:
    formula_ = parse_prop_formula(formula)
    dual_ = parse_prop_formula(dual)

    for interp in iter_interpretations(formula_):
        assert evaluate_prop_formula(formula_, interp) != evaluate_prop_formula(dual_, interp)

    result = dualize_formula_prop(formula_)
    assert result == dual_


@pytest_parametrize_kwargs(
    dict(formula='∀x.¬p¹(x)',     dual='∃x.p¹(x)'),
    dict(formula='∃x.¬p¹(x)',     dual='∀x.p¹(x)'),
    dict(formula='∀x.∃y.(x = y)', dual='∃x.∀y.¬(x = y)'),
)
def test_dualize_formula_quantifiers_order(formula: str, dual: str, dummy_signature: FormalLogicSignature) -> None:
    formula_ = parse_formula(formula, dummy_signature)
    dual_ = parse_formula(dual, dummy_signature)

    result = dualize_formula(formula_)
    assert result == dual_
