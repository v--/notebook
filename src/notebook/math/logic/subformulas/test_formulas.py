from typing import TYPE_CHECKING

from notebook.math.logic.parsing import parse_formula
from notebook.support.pytest import pytest_parametrize_kwargs

from .formulas import is_subformula


if TYPE_CHECKING:
    from notebook.math.logic.signature import FormalLogicSignature


@pytest_parametrize_kwargs(
    dict(formula='(x = y)', subformula='(x = y)'),
    dict(formula='∀x.p¹(x)', subformula='p¹(x)'),
    dict(formula='∀x.∃y.p²(x, y)', subformula='∃y.p²(x, y)'),
    dict(
        formula='((∀y.p¹(y) ∨ q¹(x)) ∧ ∃y.r¹(y))',
        subformula='q¹(x)',
    ),
)
def test_is_subformula_success(formula: str, subformula: str, dummy_signature: FormalLogicSignature) -> None:
    assert is_subformula(
        parse_formula(formula, dummy_signature),
        parse_formula(subformula, dummy_signature),
    )
