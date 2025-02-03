from collections.abc import Mapping

import pytest

from ....support.pytest import pytest_parametrize_kwargs
from ....support.schemas import SchemaInferenceError
from ..parsing import (
    TypingStyle,
    parse_pure_term,
    parse_pure_term_schema,
    parse_term,
    parse_term_placeholder,
    parse_term_schema,
    parse_variable,
    parse_variable_placeholder,
)
from ..type_systems import HOL_SIGNATURE
from .base import LambdaSchemaInstantiation
from .term_inference import (
    infer_instantiation_from_term,
)


@pytest_parametrize_kwargs(
    dict(
        schema='x',
        term='y',
        variable_mapping={'x': 'y'},
        term_mapping={}
    ),
    dict(
        schema='M',
        term='y',
        variable_mapping={},
        term_mapping={'M': 'y'}
    ),
    dict(
        schema='(xx)',
        term='(yy)',
        variable_mapping={'x': 'y'},
        term_mapping={}
    ),
    dict(
        schema='(xM)',
        term='(yy)',
        variable_mapping={'x': 'y'},
        term_mapping={'M': 'y'}
    ),
    dict(
        schema='(λx.M)',
        term='(λy.y)',
        variable_mapping={'x': 'y'},
        term_mapping={'M': 'y'}
    ),
)
def test_build_success(
    term: str,
    schema: str,
    variable_mapping: Mapping[str, str],
    term_mapping: Mapping[str, str],
) -> None:
    instantiation = infer_instantiation_from_term(parse_pure_term_schema(schema, typing=TypingStyle.implicit), parse_pure_term(term))
    expected = LambdaSchemaInstantiation(
        variable_mapping={parse_variable_placeholder(placeholder): parse_variable(value) for placeholder, value in variable_mapping.items()},
        term_mapping={parse_term_placeholder(placeholder): parse_pure_term(value) for placeholder, value in term_mapping.items()}
    )

    assert instantiation == expected


def test_constant_build_success() -> None:
    schema = parse_term_schema(HOL_SIGNATURE, 'Q', typing=TypingStyle.explicit)
    term = parse_term(HOL_SIGNATURE, 'Q', typing=TypingStyle.explicit)
    assert infer_instantiation_from_term(schema, term) == LambdaSchemaInstantiation()


def test_constant_instantiation_failure() -> None:
    with pytest.raises(SchemaInferenceError, match='Cannot match constant Q to x'):
        infer_instantiation_from_term(
            parse_term_schema(HOL_SIGNATURE, 'Q', typing=TypingStyle.implicit),
            parse_term(HOL_SIGNATURE, 'x', typing=TypingStyle.explicit)
        )


def test_variable_instantiation_failure() -> None:
    with pytest.raises(SchemaInferenceError, match=r'Cannot match variable placeholder x to \(xx\)'):
        infer_instantiation_from_term(
            parse_pure_term_schema('x', typing=TypingStyle.implicit),
            parse_pure_term('(xx)')
        )


def test_application_instantiation_failure() -> None:
    with pytest.raises(SchemaInferenceError, match=r'Cannot match application schema \(xx\) to \(λx.x\)'):
        infer_instantiation_from_term(
            parse_pure_term_schema('(xx)', typing=TypingStyle.implicit),
            parse_pure_term('(λx.x)')
        )


def test_abstraction_instantiation_failure() -> None:
    with pytest.raises(SchemaInferenceError, match=r'Cannot match abstraction schema \(λx.x\) to \(xx\)'):
        infer_instantiation_from_term(
            parse_pure_term_schema('(λx.x)', typing=TypingStyle.implicit),
            parse_pure_term('(xx)')
        )


def test_incompatible_subterm_instantiation_failure() -> None:
    with pytest.raises(SchemaInferenceError, match=r'Cannot instantiate variable placeholder x to both y and z'):
        infer_instantiation_from_term(
            parse_pure_term_schema('(xx)', typing=TypingStyle.implicit),
            parse_pure_term('(yz)')
        )
