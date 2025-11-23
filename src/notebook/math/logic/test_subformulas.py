from ...support.pytest import pytest_parametrize_kwargs
from .parsing import parse_formula
from .signature import FormalLogicSignature
from .subformulas import is_subformula


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',   subformula='(x = y)'),
    dict(formula='∀x.p¹(x)',  subformula='p¹(x)'),
    dict(
        formula='((∀y.p¹(y) ∨ q¹(x)) ∧ ∃y.r¹(y))',
        subformula='q¹(x)'
    ),
)
def test_is_subformula_success(formula: str, subformula: str, dummy_signature: FormalLogicSignature) -> None:
    assert is_subformula(
        parse_formula(formula, dummy_signature),
        parse_formula(subformula, dummy_signature)
    )
