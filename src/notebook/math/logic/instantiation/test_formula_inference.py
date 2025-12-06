from ....support.pytest import pytest_parametrize_kwargs
from ..parsing import parse_formula_schema
from ..propositional import parse_propositional_formula
from .formula_inference import is_formula_schema_instance


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
    assert is_formula_schema_instance(
        parse_formula_schema(schema),
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
    assert not is_formula_schema_instance(
        parse_formula_schema(schema),
        parse_propositional_formula(formula)
    )
