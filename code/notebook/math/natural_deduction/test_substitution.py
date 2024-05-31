import pytest

from ..fol.parsing import parse_propositional_formula
from .parsing import parse_schema
from .propositional import substitute_propositional_formulas
from .substitution import SubstitutionError, is_schema_instance


def test_substitution_application() -> None:
    def t(schema: str, **kwargs: str) -> str:
        return str(substitute_propositional_formulas(schema, **kwargs))

    assert t('φ', φ='p') == 'p'
    assert t('φ', φ='(p ∧ q)') == '(p ∧ q)'
    assert t('(φ ∧ φ)', φ='p') == '(p ∧ p)'
    assert t('(φ ∧ ψ)', φ='p', ψ='q') == '(p ∧ q)'


def test_invalid_substitution_application() -> None:
    with pytest.raises(SubstitutionError):
        substitute_propositional_formulas('φ')


def test_is_schema_instance_prop() -> None:
    def t(schema_string: str, formula_string: str) -> bool:
        schema = parse_schema(schema_string)
        formula = parse_propositional_formula(formula_string)
        return is_schema_instance(schema, formula)

    # Atomic schemas
    assert t('φ', '⊤')
    assert t('φ', 'p')
    assert t('φ', '¬p')
    assert t('φ', '(p → q)')

    # Constant schemas
    assert t('⊤', '⊤')
    assert not t('⊤', '⊥')
    assert not t('⊤', 'p')

    # Negation schemas
    assert not t('¬φ', '⊤')
    assert not t('¬φ', 'p')
    assert t('¬φ', '¬p')
    assert t('¬φ', '¬¬p')
    assert t('¬¬φ', '¬¬p')
    assert not t('¬¬φ', '¬p')

    # Connective schemas
    assert not t('(φ → ψ)', '¬p')
    assert t('(φ → ψ)', '(p → q)')
    assert t('(φ → ψ)', '(p → (q → r))')
    assert not t('(φ → ψ)', '(p ∧ q)')

    assert t('(φ → φ)', '(p → p)')
    assert not t('(φ → φ)', '(p → q)')

    assert t('(φ → (ψ → φ))', '(p → (q → p))')
    assert not t('(φ → (ψ → φ))', '(p → (q → r))')

    assert t('(φ → (ψ → φ))', '(p → ((p → p) → p))')
