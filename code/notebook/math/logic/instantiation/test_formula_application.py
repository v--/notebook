from collections.abc import Mapping

import pytest

from ....parsing.identifiers import LatinIdentifier
from ....support.pytest import pytest_parametrize_kwargs
from ....support.schemas import SchemaInstantiationError
from ..formulas import Formula
from ..parsing import (
    parse_formula,
    parse_formula_placeholder,
    parse_formula_schema,
    parse_propositional_formula,
    parse_signatureless_formula_schema,
)
from ..signature import FormalLogicSignature
from ..terms import Variable, VariablePlaceholder
from .base import FormalLogicSchemaInstantiation
from .formula_application import instantiate_formula_schema


def instantiate_propositional_schema(schema: str, **kwargs: str) -> Formula:
    instantiation = FormalLogicSchemaInstantiation(
        formula_mapping={
            parse_formula_placeholder(key): parse_propositional_formula(value) for key, value in kwargs.items()
        }
    )

    return instantiate_formula_schema(parse_signatureless_formula_schema(schema), instantiation)


@pytest_parametrize_kwargs(
    dict(
        schema='φ',
        mapping=dict(φ='p'),
        expected='p'
    ),
    dict(
        schema='φ',
        mapping=dict(φ='(p ∧ q)'),
        expected='(p ∧ q)'
    ),
    dict(
        schema='(φ ∧ φ)',
        mapping=dict(φ='p'),
        expected='(p ∧ p)'
    ),
    dict(
        schema='(φ ∧ ψ)',
        mapping=dict(φ='p', ψ='q'),
        expected='(p ∧ q)'
    )
)
def test_instantiation(schema: str, mapping: Mapping[str, str], expected: str) -> None:
    assert instantiate_propositional_schema(schema, **mapping) == parse_propositional_formula(expected)


def test_placeholder_instantiation_failure() -> None:
    with pytest.raises(SchemaInstantiationError, match='No specification of how to instantiate the formula placeholder φ'):
        instantiate_formula_schema(
            parse_signatureless_formula_schema('φ'),
            FormalLogicSchemaInstantiation()
        )


def test_instantiation_with_substitution(dummy_signature: FormalLogicSignature) -> None:
    schema = parse_formula_schema(dummy_signature, 'φ[x ↦ g₀]')

    instantiation = FormalLogicSchemaInstantiation(
        formula_mapping={parse_formula_placeholder('φ'): parse_formula(dummy_signature, '(f₀ = x)')},
        variable_mapping={VariablePlaceholder(LatinIdentifier('x')): Variable(LatinIdentifier('x'))}
    )

    instance = instantiate_formula_schema(schema, instantiation)
    assert str(instance) == '(f₀ = g₀)'
