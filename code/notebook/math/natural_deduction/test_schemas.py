from ..fol.parsing.parser import parse_formula
from ..fol.signature import FOLSignature
from .parsing.parser import parse_placeholder
from .schemas import is_schema_instance


def test_is_schema_instance_prop(propositional_signature: FOLSignature) -> None:
    def t(placeholder_string: str, formula_string: str) -> bool:
        placeholder = parse_placeholder(placeholder_string)
        formula = parse_formula(propositional_signature, formula_string)
        return is_schema_instance(placeholder, formula)

    # Atomic placeholders
    assert t('Φ', '⊤')
    assert t('Φ', 'p')
    assert t('Φ', '¬p')
    assert t('Φ', '(p → q)')

    # Constant placeholders
    assert t('⊤', '⊤')
    assert not t('⊤', '⊥')
    assert not t('⊤', 'p')

    # Negation placeholders
    assert not t('¬Φ', '⊤')
    assert not t('¬Φ', 'p')
    assert t('¬Φ', '¬p')
    assert t('¬Φ', '¬¬p')
    assert t('¬¬Φ', '¬¬p')
    assert not t('¬¬Φ', '¬p')

    # Connective placeholders
    assert not t('(Φ → Ψ)', '¬p')
    assert t('(Φ → Ψ)', '(p → q)')
    assert t('(Φ → Ψ)', '(p → (q → r))')
    assert not t('(Φ → Ψ)', '(p ∧ q)')

    assert t('(Φ → Φ)', '(p → p)')
    assert not t('(Φ → Φ)', '(p → q)')

    assert t('(Φ → (Ψ → Φ))', '(p → (q → p))')
    assert not t('(Φ → (Ψ → Φ))', '(p → (q → r))')

    assert t('(Φ → (Ψ → Φ))', '(p → ((p → p) → p))')
