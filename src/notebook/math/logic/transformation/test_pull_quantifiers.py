from ....support.pytest import pytest_parametrize_kwargs
from ..parsing import parse_formula
from ..signature import FormalLogicSignature
from .pull_quantifiers import pull_quantifiers


@pytest_parametrize_kwargs(
    # Atomic
    dict(formula='⊤',  expected=None),
    dict(formula='(x = y)',  expected=None),

    # Negation
    dict(formula='¬∀x.p¹(x)', expected='∃x.¬p¹(x)'),
    dict(formula='¬∀x.∀y.p²(x, y)', expected='∃x.∃y.¬p²(x, y)'),
    dict(formula='¬∃x.p¹(x)',  expected='∀x.¬p¹(x)'),
    dict(formula='¬∃x.¬p¹(x)', expected='∀x.p¹(x)'),

    # Conjunctions and disjunctions
    dict(formula='(∀x.p¹(x) ∨ q¹(y))', expected='∀x.(p¹(x) ∨ q¹(y))'),
    dict(formula='(∀x.p¹(x) ∨ q¹(x))', expected='∀a.(p¹(a) ∨ q¹(x))'),
    dict(formula='(∀x.p¹(x) ∨ q²(a, x))', expected='∀b.(p¹(b) ∨ q²(a, x))'),
    dict(
        formula='(∀x.p¹(x) ∨ ∀x.q¹(x))',
        expected='∀x.∀a.(p¹(x) ∨ q¹(a))'
    ),
    dict(
        formula='((∃x.p¹(x) ∧ ∃y.q¹(y)) ∨ (∃x.p¹(x) ∧ ∃y.q¹(y)))',
        expected='∃x.∃y.∃a.∃b.((p¹(x) ∧ q¹(y)) ∨ (p¹(a) ∧ q¹(b)))'
    ),
    dict(
        formula='((∀x.p¹(x) ∨ q¹(x)) ∧ ∃a.r¹(a))',
        expected='∀a.∃b.((p¹(a) ∨ q¹(x)) ∧ r¹(b))'
    ),

    # Conditionals
    dict(formula='(p¹(x) → q¹(x))', expected=None),
    dict(formula='(∀x.p¹(x) → q¹(x))', expected='∃a.(p¹(a) → q¹(x))'),
    dict(formula='(∃x.p¹(x) → q¹(x))', expected='∀a.(p¹(a) → q¹(x))'),
    dict(formula='(p¹(x) → ∀x.q¹(x))', expected='∀a.(p¹(x) → q¹(a))'),
    dict(formula='(p¹(x) → ∃x.q¹(x))', expected='∃a.(p¹(x) → q¹(a))'),
    dict(formula='(∃x.p¹(x) → ∃x.q¹(x))', expected='∀x.∃a.(p¹(x) → q¹(a))'),

    # Biconditionals
    dict(formula='(p¹(x) ↔ q¹(x))', expected=None),
    dict(formula='(∀x.p¹(x) ↔ q¹(x))', expected='∃a.∀b.((p¹(a) → q¹(x)) ∧ (q¹(x) → p¹(b)))'),

    # Quantifiers
    dict(formula='∀x.p¹(x)', expected=None),
    dict(formula='∃x.p¹(x)', expected=None),
)
def test_pull_quantifiers(formula: str, expected: str | None, dummy_signature: FormalLogicSignature) -> None:
    formula_ = parse_formula(formula, dummy_signature)
    expected_ = formula_ if expected is None else parse_formula(expected, dummy_signature)
    expanded = pull_quantifiers(formula_)
    assert expanded == expected_
