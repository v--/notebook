from collections.abc import Mapping

import pytest

from ....support.pytest import pytest_parametrize_kwargs
from ....support.schemas import SchemaInferenceError
from ..hol import HOL_SIGNATURE
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
from .term_inference import (
    infer_instantiation_from_term,
)


@pytest_parametrize_kwargs(
    dict(
        schema='x',
        term='y',
        variable_mapping={'x': 'y'},
        term_mapping={},
        type_mapping={}
    ),
    dict(
        schema='M',
        term='y',
        variable_mapping={},
        term_mapping={'M': 'y'},
        type_mapping={}
    ),
    dict(
        schema='(xx)',
        term='(yy)',
        variable_mapping={'x': 'y'},
        term_mapping={},
        type_mapping={}
    ),
    dict(
        schema='(xM)',
        term='(yy)',
        variable_mapping={'x': 'y'},
        term_mapping={'M': 'y'},
        type_mapping={}
    ),
    dict(
        schema='(λx:τ.M)',
        term='(λy:σ.y)',
        variable_mapping={'x': 'y'},
        term_mapping={'M': 'y'},
        type_mapping={'τ': 'σ'}
    )
)
def test_infer_success(
    term: str,
    schema: str,
    variable_mapping: Mapping[str, str],
    term_mapping: Mapping[str, str],
    type_mapping: Mapping[str, str],
) -> None:
    instantiation = infer_instantiation_from_term(parse_typed_term_schema(schema), parse_typed_term(term))
    expected = LambdaSchemaInstantiation(
        variable_mapping={parse_variable_placeholder(placeholder): parse_variable(value) for placeholder, value in variable_mapping.items()},
        term_mapping={parse_term_placeholder(placeholder): parse_typed_term(value) for placeholder, value in term_mapping.items()},
        type_mapping={parse_type_placeholder(placeholder): parse_type(value) for placeholder, value in type_mapping.items()}
    )

    assert instantiation == expected


def test_constant_infer_success() -> None:
    schema = parse_typed_term_schema('Q', HOL_SIGNATURE)
    term = parse_typed_term('Q', HOL_SIGNATURE)
    assert infer_instantiation_from_term(schema, term) == LambdaSchemaInstantiation()


def test_constant_instantiation_failure() -> None:
    with pytest.raises(SchemaInferenceError, match='Cannot match constant Q to x'):
        infer_instantiation_from_term(
            parse_typed_term_schema('Q', HOL_SIGNATURE),
            parse_typed_term('x', HOL_SIGNATURE)
        )


def test_variable_instantiation_failure() -> None:
    with pytest.raises(SchemaInferenceError, match=r'Cannot match variable placeholder x to \(xx\)'):
        infer_instantiation_from_term(
            parse_typed_term_schema('x'),
            parse_typed_term('(xx)')
        )


def test_application_instantiation_failure() -> None:
    with pytest.raises(SchemaInferenceError, match=r'Cannot match application schema \(xx\) to \(λx:τ.x\)'):
        infer_instantiation_from_term(
            parse_typed_term_schema('(xx)'),
            parse_typed_term('(λx:τ.x)')
        )


def test_abstraction_instantiation_failure() -> None:
    with pytest.raises(SchemaInferenceError, match=r'Cannot match abstraction schema \(λx:τ.x\) to \(xx\)'):
        infer_instantiation_from_term(
            parse_typed_term_schema('(λx:τ.x)'),
            parse_typed_term('(xx)')
        )


def test_abstraction_annotation_success() -> None:
    schema = parse_typed_term_schema('(λx:τ.x)')
    term = parse_typed_term('(λx:ι.x)', HOL_SIGNATURE)
    assert infer_instantiation_from_term(schema, term) == LambdaSchemaInstantiation(
        variable_mapping={parse_variable_placeholder('x'): parse_variable('x')},
        type_mapping={parse_type_placeholder('τ'): parse_type('ι', HOL_SIGNATURE)}
    )


def test_incompatible_subterm_instantiation_failure() -> None:
    with pytest.raises(SchemaInferenceError, match=r'Cannot instantiate variable placeholder x to both y and z'):
        infer_instantiation_from_term(
            parse_typed_term_schema('(xx)'),
            parse_typed_term('(yz)')
        )
