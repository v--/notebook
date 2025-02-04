from ...support.pytest import pytest_parametrize_kwargs
from .parsing import parse_formula
from .signature import FormalLogicSignature
from .subformulas import is_subformula


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',   subformula='(x = y)'),
    dict(formula='∀x.p₁(x)',  subformula='p₁(x)'),
    dict(
        formula='((∀y.p₁(y) ∨ q₁(x)) ∧ ∃y.r₁(y))',
        subformula='q₁(x)'
    ),
)
def test_is_subformula_success(formula: str, subformula: str, dummy_signature: FormalLogicSignature) -> None:
    assert is_subformula(
        parse_formula(dummy_signature, formula),
        parse_formula(dummy_signature, subformula)
    )
