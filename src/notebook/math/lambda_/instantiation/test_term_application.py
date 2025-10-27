from collections.abc import Mapping

import pytest

from ....support.pytest import pytest_parametrize_kwargs
from ....support.schemas import SchemaInstantiationError
from ..algebraic_types import SIMPLE_ALGEBRAIC_SIGNATURE
from ..parsing import (
    parse_term_placeholder,
    parse_type,
    parse_type_placeholder,
    parse_typed_term,
    parse_typed_term_schema,
    parse_variable,
    parse_variable_placeholder,
)
from .base import LambdaSchemaInstantiation
from .term_application import instantiate_term_schema


@pytest_parametrize_kwargs(
    dict(
        schema='x',
        expected='y',
        variable_mapping={'x': 'y'},
        term_mapping={},
        type_mapping={}
    ),
    dict(
        schema='y',
        expected='y',
        variable_mapping={'y': 'y'},
        term_mapping={},
        type_mapping={}
    ),
    dict(
        schema='(λx:τ.x)',
        expected='(λy:σ.y)',
        variable_mapping={'x': 'y'},
        term_mapping={},
        type_mapping={'τ': 'σ'}
    ),
    dict(
        schema='(Ix)',
        expected='((λx:τ.x)y)',
        variable_mapping={'x': 'y'},
        term_mapping={'I': '(λx:τ.x)'},
        type_mapping={}
    )
)
def test_instantiation_success(
    expected: str,
    schema: str,
    variable_mapping: Mapping[str, str],
    term_mapping: Mapping[str, str],
    type_mapping: Mapping[str, str],
) -> None:
    instantiation = LambdaSchemaInstantiation(
        variable_mapping={parse_variable_placeholder(placeholder): parse_variable(value) for placeholder, value in variable_mapping.items()},
        term_mapping={parse_term_placeholder(placeholder): parse_typed_term(value) for placeholder, value in term_mapping.items()},
        type_mapping={parse_type_placeholder(placeholder): parse_type(value) for placeholder, value in type_mapping.items()}
    )

    assert instantiate_term_schema(parse_typed_term_schema(schema), instantiation) == parse_typed_term(expected)


def test_constant_instantiation_success() -> None:
    instantiation = LambdaSchemaInstantiation()
    u = parse_typed_term_schema('U₊', SIMPLE_ALGEBRAIC_SIGNATURE)
    assert instantiate_term_schema(u, instantiation) == u


def test_variable_instantiation_failure() -> None:
    instantiation = LambdaSchemaInstantiation()

    with pytest.raises(SchemaInstantiationError, match='No specification of how to instantiate the variable placeholder x'):
        instantiate_term_schema(parse_typed_term_schema('x'), instantiation)


def test_term_instantiation_failure() -> None:
    instantiation = LambdaSchemaInstantiation()

    with pytest.raises(SchemaInstantiationError, match='No specification of how to instantiate the term placeholder M'):
        instantiate_term_schema(parse_typed_term_schema('M'), instantiation)


def test_abstraction_annotation_success() -> None:
    schema = parse_typed_term_schema('(λx:τ.x)')
    instantiation = LambdaSchemaInstantiation(
        variable_mapping={parse_variable_placeholder('x'): parse_variable('x')},
        type_mapping={parse_type_placeholder('τ'): parse_type('τ')}
    )

    expected = parse_typed_term('(λx:τ.x)')
    assert instantiate_term_schema(schema, instantiation) == expected


def test_abstraction_annotation_failure() -> None:
    with pytest.raises(SchemaInstantiationError, match=r'No specification of how to instantiate the type placeholder τ'):
        schema = parse_typed_term_schema('(λx:τ.x)')
        instantiation = LambdaSchemaInstantiation(
            variable_mapping={parse_variable_placeholder('x'): parse_variable('x')},
        )

        instantiate_term_schema(schema, instantiation)
