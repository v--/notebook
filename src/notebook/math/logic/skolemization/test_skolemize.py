from ....support.pytest import pytest_parametrize_kwargs
from ...rings.modular import Z5
from ..parsing import parse_formula
from ..signature import FormalLogicSignature
from ..structure import evaluate_formula
from ..theories.arithmetic import ARITHMETIC_SIGNATURE, ModularArithmeticStructure
from .prenex_formula import formula_to_prenex_form
from .skolemize import skolemize


@pytest_parametrize_kwargs(
    dict(formula='∀x.p¹(x)', expected=None),
    dict(formula='∀x.∃y.p²(x, y)', expected='∀x.p²(x, a¹(x))'),
    dict(formula='∀x.∃y.∀z.∃t.p²(f²(x, y), f²(z, t))', expected='∀x.∀z.p²(f²(x, a¹(x)), f²(z, a²(x, z)))'),
)
def test_skolemize_without_model(formula: str, expected: str | None, dummy_signature: FormalLogicSignature) -> None:
    prenex_formula = formula_to_prenex_form(parse_formula(formula, dummy_signature))
    skolemization = skolemize(prenex_formula, dummy_signature)
    expected_ = prenex_formula.get_quantified() if expected is None else parse_formula(expected, skolemization.signature)
    assert skolemization.prenex_formula.get_quantified() == expected_


def test_skolemize_of_z5_predecessor() -> None:
    model = ModularArithmeticStructure(Z5)
    predecessor_formula = parse_formula('∀x.∃y.(Sy = x)', ARITHMETIC_SIGNATURE)
    prenex_formula = formula_to_prenex_form(predecessor_formula)
    assert evaluate_formula(predecessor_formula, model)

    skolemization = skolemize(prenex_formula, ARITHMETIC_SIGNATURE, model)
    skolemized_formula = skolemization.prenex_formula.get_quantified()
    assert evaluate_formula(skolemized_formula, skolemization.model)

    expected_formula = parse_formula('∀x.(Sa¹(x) = x)', skolemization.signature)
    assert skolemized_formula == expected_formula
