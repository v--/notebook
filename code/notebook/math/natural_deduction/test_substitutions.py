from typing import cast

import pytest

from ..fol.parsing.parser import parse_formula
from ..fol.signature import FOLSignature
from .parsing.parser import parse_placeholder
from .placeholders import AtomicFormulaPlaceholder
from .substitutions import SubstitutionError, UniformSubstitution, is_schema_instance


def test_substitution_application(propositional_signature: FOLSignature) -> None:
    def t(placeholder: str, mapping: dict[str, str]) -> str:
        parsed_placeholder = parse_placeholder(placeholder)
        substitution = UniformSubstitution({
            cast(AtomicFormulaPlaceholder, parse_placeholder(src)): parse_formula(propositional_signature, dest)
            for src, dest in mapping.items()
        })

        return str(substitution.apply_to(parsed_placeholder))

    assert t('φ', {'φ': 'p'}) == 'p'
    assert t('φ', {'φ': '(p ∧ q)'}) == '(p ∧ q)'
    assert t('(φ ∧ φ)', {'φ': 'p'}) == '(p ∧ p)'
    assert t('(φ ∧ ψ)', {'φ': 'p', 'ψ': 'q'}) == '(p ∧ q)'


def test_invalid_substitution_application() -> None:
    with pytest.raises(SubstitutionError):
        UniformSubstitution({}).apply_to(
            parse_placeholder('φ')
        )


def test_is_schema_instance_prop(propositional_signature: FOLSignature) -> None:
    def t(placeholder_string: str, formula_string: str) -> bool:
        placeholder = parse_placeholder(placeholder_string)
        formula = parse_formula(propositional_signature, formula_string)
        return is_schema_instance(placeholder, formula)

    # Atomic placeholders
    assert t('φ', '⊤')
    assert t('φ', 'p')
    assert t('φ', '¬p')
    assert t('φ', '(p → q)')

    # Constant placeholders
    assert t('⊤', '⊤')
    assert not t('⊤', '⊥')
    assert not t('⊤', 'p')

    # Negation placeholders
    assert not t('¬φ', '⊤')
    assert not t('¬φ', 'p')
    assert t('¬φ', '¬p')
    assert t('¬φ', '¬¬p')
    assert t('¬¬φ', '¬¬p')
    assert not t('¬¬φ', '¬p')

    # Connective placeholders
    assert not t('(φ → ψ)', '¬p')
    assert t('(φ → ψ)', '(p → q)')
    assert t('(φ → ψ)', '(p → (q → r))')
    assert not t('(φ → ψ)', '(p ∧ q)')

    assert t('(φ → φ)', '(p → p)')
    assert not t('(φ → φ)', '(p → q)')

    assert t('(φ → (ψ → φ))', '(p → (q → p))')
    assert not t('(φ → (ψ → φ))', '(p → (q → r))')

    assert t('(φ → (ψ → φ))', '(p → ((p → p) → p))')
