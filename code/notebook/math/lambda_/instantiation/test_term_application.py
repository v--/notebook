from collections.abc import Mapping

import pytest

from ....support.pytest import pytest_parametrize_kwargs
from ....support.schemas import SchemaInstantiationError
from ..parsing import (
    TypingStyle,
    parse_pure_term,
    parse_pure_term_schema,
    parse_term_placeholder,
    parse_term_schema,
    parse_variable,
    parse_variable_placeholder,
)
from ..type_systems import HOL_SIGNATURE
from .base import LambdaSchemaInstantiation
from .term_application import (
    instantiate_term_schema,
)


@pytest_parametrize_kwargs(
    dict(
        schema='x',
        expected='y',
        variable_mapping={'x': 'y'},
        term_mapping={}
    ),
    dict(
        schema='y',
        expected='y',
        variable_mapping={'y': 'y'},
        term_mapping={}
    ),
    dict(
        schema='(Ix)',
        expected='((λx.x)y)',
        variable_mapping={'x': 'y'},
        term_mapping={'I': '(λx.x)'}
    )
)
def test_instantiation_success(
    expected: str,
    schema: str,
    variable_mapping: Mapping[str, str],
    term_mapping: Mapping[str, str],
) -> None:
    instantiation = LambdaSchemaInstantiation(
        variable_mapping={parse_variable_placeholder(placeholder): parse_variable(value) for placeholder, value in variable_mapping.items()},
        term_mapping={parse_term_placeholder(placeholder): parse_pure_term(value) for placeholder, value in term_mapping.items()}
    )

    assert instantiate_term_schema(parse_pure_term_schema(schema, typing=TypingStyle.implicit), instantiation) == parse_pure_term(expected)


def test_constant_instantiation_success() -> None:
    instantiation = LambdaSchemaInstantiation()
    q = parse_term_schema(HOL_SIGNATURE, 'Q', typing=TypingStyle.explicit)
    assert instantiate_term_schema(q, instantiation) == q


def test_variable_instantiation_failure() -> None:
    instantiation = LambdaSchemaInstantiation()

    with pytest.raises(SchemaInstantiationError, match='No specification of how to instantiate the variable placeholder x'):
        instantiate_term_schema(parse_pure_term_schema('x', typing=TypingStyle.implicit), instantiation)


def test_term_instantiation_failure() -> None:
    instantiation = LambdaSchemaInstantiation()

    with pytest.raises(SchemaInstantiationError, match='No specification of how to instantiate the term placeholder M'):
        instantiate_term_schema(parse_pure_term_schema('M', typing=TypingStyle.implicit), instantiation)
