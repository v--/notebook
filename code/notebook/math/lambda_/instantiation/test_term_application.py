from collections.abc import Mapping

import pytest

from ....support.pytest import pytest_parametrize_kwargs
from ....support.schemas import SchemaInstantiationError
from ..parsing import (
    parse_pure_term,
    parse_pure_term_schema,
    parse_term,
    parse_term_placeholder,
    parse_term_schema,
    parse_type,
    parse_type_placeholder,
    parse_variable,
    parse_variable_placeholder,
)
from ..type_systems import HOL_SIGNATURE
from ..typing import TypingStyle
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

    assert instantiate_term_schema(parse_pure_term_schema(schema, TypingStyle.implicit), instantiation) == parse_pure_term(expected)


def test_constant_instantiation_success() -> None:
    instantiation = LambdaSchemaInstantiation()
    q = parse_term_schema(HOL_SIGNATURE, 'Q', TypingStyle.explicit)
    assert instantiate_term_schema(q, instantiation) == q


def test_variable_instantiation_failure() -> None:
    instantiation = LambdaSchemaInstantiation()

    with pytest.raises(SchemaInstantiationError, match='No specification of how to instantiate the variable placeholder x'):
        instantiate_term_schema(parse_pure_term_schema('x', TypingStyle.implicit), instantiation)


def test_term_instantiation_failure() -> None:
    instantiation = LambdaSchemaInstantiation()

    with pytest.raises(SchemaInstantiationError, match='No specification of how to instantiate the term placeholder M'):
        instantiate_term_schema(parse_pure_term_schema('M', TypingStyle.implicit), instantiation)


def test_abstraction_annotation_success() -> None:
    schema = parse_pure_term_schema('(λx:α.x)', TypingStyle.explicit)
    instantiation = LambdaSchemaInstantiation(
        variable_mapping={parse_variable_placeholder('x'): parse_variable('x')},
        type_mapping={parse_type_placeholder('α'): parse_type(HOL_SIGNATURE, 'ι')}
    )

    expected = parse_term(HOL_SIGNATURE, '(λx:ι.x)', TypingStyle.explicit)
    assert instantiate_term_schema(schema, instantiation) == expected


def test_abstraction_annotation_failure() -> None:
    with pytest.raises(SchemaInstantiationError, match=r'No specification of how to instantiate the type placeholder α'):
        schema = parse_pure_term_schema('(λx:α.x)', TypingStyle.explicit)
        instantiation = LambdaSchemaInstantiation(
            variable_mapping={parse_variable_placeholder('x'): parse_variable('x')},
        )

        instantiate_term_schema(schema, instantiation)


def test_typed_instantiation_on_untyped_schema() -> None:
    with pytest.raises(SchemaInstantiationError, match='An untyped schema was provided, but the instantiation features typed terms'):
        schema = parse_pure_term_schema('(λx.M)', TypingStyle.implicit)
        instantiation = LambdaSchemaInstantiation(
            variable_mapping={parse_variable_placeholder('x'): parse_variable('x')},
            term_mapping={parse_term_placeholder('M'): parse_term(HOL_SIGNATURE, '(λy:ι.y)', TypingStyle.explicit)},
            type_mapping={parse_type_placeholder('α'): parse_type(HOL_SIGNATURE, 'ι')}
        )

        instantiate_term_schema(schema, instantiation)


def test_untyped_instantiation_on_typed_schema() -> None:
    with pytest.raises(SchemaInstantiationError, match='A typed schema was provided, but the instantiation features untyped terms'):
        schema = parse_pure_term_schema('(λx:α.M)', TypingStyle.explicit)
        instantiation = LambdaSchemaInstantiation(
            variable_mapping={parse_variable_placeholder('x'): parse_variable('x')},
            term_mapping={parse_term_placeholder('M'): parse_term(HOL_SIGNATURE, '(λy.y)', TypingStyle.implicit)},
            type_mapping={parse_type_placeholder('α'): parse_type(HOL_SIGNATURE, 'ι')}
        )

        instantiate_term_schema(schema, instantiation)
