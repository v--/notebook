
lazy from collections.abc import Mapping

from notebook.math.logic.parsing import parse_formula
from notebook.math.logic.propositional.parsing import parse_prop_formula, parse_prop_variable
from notebook.support.pytest import pytest_parametrize_kwargs
lazy from notebook.math.logic.signature import FormalLogicSignature

from .formula_application import translate_prop_formula


@pytest_parametrize_kwargs(
    dict(
        formula='p',
        mapping=dict(p='⊤'),
        expected='⊤',
    ),
    dict(
        formula='(p ∧ q)',
        mapping=dict(p='p⁰', q='q⁰'),
        expected='(p⁰ ∧ q⁰)',
    ),
)
def test_translate_prop_formula(
    formula: str,
    mapping: Mapping[str, str],
    expected: str,
    dummy_signature: FormalLogicSignature,
) -> None:
    formula_ = parse_prop_formula(formula)
    expected_ = parse_formula(expected, dummy_signature)
    result = translate_prop_formula(
        formula_,
        {parse_prop_variable(key): parse_formula(value, dummy_signature) for key, value in mapping.items()},
    )

    assert result == expected_
