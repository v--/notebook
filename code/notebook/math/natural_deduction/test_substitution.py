import pytest

from ...support.pytest import pytest_parametrize_kwargs
from ..fol.parsing import parse_propositional_formula
from .parsing import parse_schema
from .propositional import substitute_propositional_formulas
from .substitution import SubstitutionError, is_schema_instance


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
def test_substitution_application(schema: str, mapping: dict[str, str], expected: str) -> None:
    assert substitute_propositional_formulas(schema, **mapping) == parse_propositional_formula(expected)


def test_invalid_substitution_application() -> None:
    with pytest.raises(SubstitutionError):
        substitute_propositional_formulas('φ')


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
        parse_schema(schema),
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
        parse_schema(schema),
        parse_propositional_formula(formula)
    )
