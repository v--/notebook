from typing import Any

from notebook.math.lambda_.hol import common
from notebook.math.lambda_.hol.expression import HolExpression
from notebook.math.lambda_.hol.theories.arithmetic import ARITHMETIC_SIGNATURE, ModularArithmeticStructure
from notebook.math.lambda_.parsing.parser import parse_typed_term
from notebook.math.rings.modular import Z2
from notebook.support.pytest import pytest_parametrize_kwargs

from .evaluation import evaluate_hol_expression


@pytest_parametrize_kwargs(
    # ⊤
    dict(formula='L⊤',                    value=True),
    # ⊤ ∧ ⊥
    dict(formula='((L∧L⊤)L⊥)',            value=False),
    # (λx:ι.S⁺x)0
    dict(formula='((λx:ι.(S⁺x))0)',       value=Z2(1)),
    # ∀x:ι.(x = x)
    dict(formula='(L∀(λx:ι.((L=x)x)))',   value=True),
    # ∀p:(ι → ο).p(0)
    dict(formula='(L∀(λp:(ι → ο).(p0)))', value=False),
    # ∃p:(ι → ο).p(0)
    dict(formula='(L∃(λp:(ι → ο).(p0)))', value=True),
    # 0 × S⁺(0)
    dict(formula='((×0)(S⁺0))',           value=Z2(0)),
    # 0 ≤ S⁺(0)
    dict(formula='((≤0)(S⁺0))',           value=True),
)
def test_evaluate_hol_expression(formula: str, value: Any) -> None:  # noqa: ANN401
    model = ModularArithmeticStructure(Z2)
    formula_ = HolExpression(
        parse_typed_term(formula, ARITHMETIC_SIGNATURE),
        common.prop,
    )

    assert evaluate_hol_expression(formula_, model) == value
