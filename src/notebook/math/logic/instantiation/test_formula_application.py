from collections.abc import Mapping

import pytest

from ....support.pytest import pytest_parametrize_kwargs
from ....support.schemas import SchemaInstantiationError
from ..formulas import Formula
from ..parsing import parse_formula_placeholder, parse_formula_schema
from ..propositional import convert_to_prop_formula, parse_prop_formula
from .base import AtomicLogicSchemaInstantiation
from .formula_application import instantiate_formula_schema


def instantiate_prop_schema(schema: str, **kwargs: str) -> Formula:
    instantiation = AtomicLogicSchemaInstantiation(
        formula_mapping={
            parse_formula_placeholder(key): parse_prop_formula(value) for key, value in kwargs.items()
        }
    )

    return convert_to_prop_formula(
        instantiate_formula_schema(parse_formula_schema(schema), instantiation)
    )


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
    assert instantiate_prop_schema(schema, **mapping) == parse_prop_formula(expected)


def test_placeholder_instantiation_failure() -> None:
    with pytest.raises(SchemaInstantiationError, match='No specification of how to instantiate the formula placeholder φ'):
        instantiate_formula_schema(
            parse_formula_schema('φ'),
            AtomicLogicSchemaInstantiation()
        )
