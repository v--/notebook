from collections.abc import Mapping

import pytest

from ...parsing.identifiers import LatinIdentifier
from ...support.pytest import pytest_parametrize_kwargs
from .formulas import Formula
from .instantiation import (
    SchemaInstantiation,
    SchemaInstantiationError,
    instantiate_schema,
    is_schema_instance,
)
from .parsing import (
    parse_formula,
    parse_formula_placeholder,
    parse_formula_schema,
    parse_general_formula_schema,
    parse_propositional_formula,
)
from .signature import FOLSignature
from .terms import Variable, VariablePlaceholder


def instantiate_propositional_schema(schema: str, **kwargs: str) -> Formula:
    instantiation = SchemaInstantiation(
        formula_mapping={
            parse_formula_placeholder(key): parse_propositional_formula(value) for key, value in kwargs.items()
        }
    )

    return instantiate_schema(parse_general_formula_schema(schema), instantiation)


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


def test_invalid_instantiation() -> None:
    with pytest.raises(SchemaInstantiationError):
        instantiate_propositional_schema('φ')


def test_instantiation_with_substitution(dummy_signature: FOLSignature) -> None:
    schema = parse_formula_schema(dummy_signature, 'φ[x ↦ g₀]')

    instantiation = SchemaInstantiation(
        formula_mapping={parse_formula_placeholder('φ'): parse_formula(dummy_signature, '(f₀ = x)')},
        variable_mapping={VariablePlaceholder(LatinIdentifier('x')): Variable(LatinIdentifier('x'))}
    )

    instance = instantiate_schema(schema, instantiation)
    assert str(instance) == '(f₀ = g₀)'


@pytest_parametrize_kwargs(
    # Atomic schemas
    dict(schema='φ', formula='⊤'),
    dict(schema='φ', formula='p'),
    dict(schema='φ', formula='¬p'),
    dict(schema='φ', formula='(p → q)'),

    # Constant schemas
    dict(schema='⊤', formula='⊤'),

    # Negation schemas
    dict(schema='¬φ', formula='¬p'),
    dict(schema='¬φ', formula='¬¬p'),
    dict(schema='¬¬φ', formula='¬¬p'),

    # Connective schemas
    dict(schema='(φ → ψ)', formula='(p → q)'),
    dict(schema='(φ → ψ)', formula='(p → (q → r))'),
    dict(schema='(φ → φ)', formula='(p → p)'),
    dict(schema='(φ → (ψ → φ))', formula='(p → (q → p))'),
    dict(schema='(φ → (ψ → φ))', formula='(p → ((p → p) → p))')
)
def test_is_schema_instance_success(schema: str, formula: str) -> None:
    assert is_schema_instance(
        parse_general_formula_schema(schema),
        parse_propositional_formula(formula)
    )


@pytest_parametrize_kwargs(
    # Constant schemas
    dict(schema='⊤', formula='⊥'),
    dict(schema='⊤', formula='p'),

    # Negation schemas
    dict(schema='¬φ', formula='⊤'),
    dict(schema='¬φ', formula='p'),
    dict(schema='¬¬φ', formula='¬p'),

    # Connective schemas
    dict(schema='(φ → ψ)', formula='¬p'),
    dict(schema='(φ → ψ)', formula='(p ∧ q)'),
    dict(schema='(φ → φ)', formula='(p → q)'),
    dict(schema='(φ → (ψ → φ))', formula='(p → (q → r))'),
)
def test_is_schema_instance_failure(schema: str, formula: str) -> None:
    assert not is_schema_instance(
        parse_general_formula_schema(schema),
        parse_propositional_formula(formula)
    )
