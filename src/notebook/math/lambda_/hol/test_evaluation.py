from ....support.pytest import pytest_parametrize_kwargs
from ...rings.modular import Z2
from ..parsing.parser import parse_typed_term
from ..types import BaseType
from .evaluation import evaluate_hol_expression
from .expressions import HolExpression
from .modular import ARITHMETIC_SIGNATURE, ModularArithmeticStructure
from .symbols import common_types


@pytest_parametrize_kwargs(
    # ⊤
    dict(formula='H⊤',                  value=True),
    # ⊤ ∧ ⊥
    dict(formula='((H∧H⊤)H⊥)',          value=False),
    # ∀x:ι.(x = x)
    dict(formula='(H∀(λx:ι.((H=x)x)))', value=True),
    # (λx:ι.S⁺x)0
    dict(formula='((λx:ι.(S⁺x))0)',     value=Z2(1)),
    # 0 × S⁺(0)
    dict(formula='((×0)(S⁺0))',         value=Z2(0)),
    # 0 ≤ S⁺(0)
    dict(formula='((≤0)(S⁺0))',         value=True),
)
def test_evaluate_hol_expression(formula: str, value: Z2 | bool) -> None:  # noqa: FBT001
    model = ModularArithmeticStructure(Z2)
    formula_ = HolExpression(
        parse_typed_term(formula, ARITHMETIC_SIGNATURE),
        BaseType(common_types.prop)
    )

    assert evaluate_hol_expression(formula_, model) == value
