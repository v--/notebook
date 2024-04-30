import pytest

from .parsing import parse_formula
from .pnf import (
    PNFError,
    is_formula_in_pnf,
    is_formula_quantifierless,
    move_quantifiers,
    push_negations,
    remove_conditionals,
    to_pnf,
)
from .signature import FOLSignature


def test_is_formula_quantifierless(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> bool:
        return is_formula_quantifierless(parse_formula(dummy_signature, string))

    assert t('⊤')
    assert t('(ξ = η)')
    assert t('((ξ = η) ∨ ¬(ξ = η))')
    assert not t('∀ξ.p₁(η)')
    assert not t('¬∀ξ.p₁(η)')


def test_is_formula_in_pnf(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> bool:
        return is_formula_in_pnf(parse_formula(dummy_signature, string))

    assert t('(ξ = η)')
    assert t('∀ξ.p₁(η)')
    assert t('∀ζ.∃ζ.(¬r₁(η) ∧ ¬r₂(ζ, η))')
    assert not t('¬∀ξ.p₁(η)')
    assert not t('∀η.∃ζ.(¬p₁(ζ) ∧ ∀ξ.(q₂(ζ, ξ) → ¬r₂(η, ξ)))')


def test_remove_conditionals(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> str:
        return str(remove_conditionals(parse_formula(dummy_signature, string)))

    assert t('(ξ = η)') == '(ξ = η)'
    assert t('(p₁(ξ) ∨ q₁(η))') == '(p₁(ξ) ∨ q₁(η))'
    assert t('(p₁(ξ) → q₁(η))') == '(¬p₁(ξ) ∨ q₁(η))'
    assert t('(p₁(ξ) ↔ q₁(η))') == '((¬p₁(ξ) ∨ q₁(η)) ∧ (p₁(ξ) ∨ ¬q₁(η)))'
    assert t('¬(p₁(ξ) → q₁(η))') == '¬(¬p₁(ξ) ∨ q₁(η))'
    assert t('∀η.∃ζ.¬(p₁(ξ) → q₁(η))') == '∀η.∃ζ.¬(¬p₁(ξ) ∨ q₁(η))'


def test_move_negations(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> str:
        return str(push_negations(parse_formula(dummy_signature, string)))

    with pytest.raises(PNFError):
        t('¬(p₁(ξ) → p₁(η))')

    with pytest.raises(PNFError):
        t('¬(p₁(ξ) ↔ p₁(η))')

    assert t('(ξ = η)') == '(ξ = η)'
    assert t('¬(ξ = η)') == '¬(ξ = η)'
    assert t('¬¬(ξ = η)') == '(ξ = η)'
    assert t('¬(p₁(ξ) ∨ ¬q₁(η))') == '(¬p₁(ξ) ∧ q₁(η))'
    assert t('¬∀η.∃ζ.(p₁(ξ) ∨ ¬q₁(η))') == '∃η.∀ζ.(¬p₁(ξ) ∧ q₁(η))'
    assert t('¬(p₁(ξ) ∨ ¬(q₁(η) ∧ ¬(∃ζ.r₁(ζ) ∨ ¬s₁(τ))))') == '(¬p₁(ξ) ∧ (q₁(η) ∧ (∀ζ.¬r₁(ζ) ∧ s₁(τ))))'


def test_move_quantifiers(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> str:
        return str(move_quantifiers(parse_formula(dummy_signature, string)))

    with pytest.raises(PNFError):
        t('¬(p₁(ξ) → p₁(η))')

    with pytest.raises(PNFError):
        t('¬(p₁(ξ) ↔ p₁(η))')

    # It is expected not to work on formulas where negations are not moved inwards.
    assert t('¬∀η.p₁(ξ)') == '¬∀η.p₁(ξ)'

    assert t('(ξ = η)') == '(ξ = η)'
    assert t('∀η.p₁(ξ)') == '∀η.p₁(ξ)'
    assert t('∀η.∀η.p₁(ξ)') == '∀η.∀η.p₁(ξ)'
    assert t('∀η.∀η.p₁(η)') == '∀η.∀η.p₁(η)'
    assert t('(∀ξ.p₁(ξ) ∨ q₁(η))') == '∀ξ₀.(p₁(ξ₀) ∨ q₁(η))'
    assert t('(∀ξ.p₁(ξ) ∨ q₁(ξ))') == '∀ξ₀.(p₁(ξ₀) ∨ q₁(ξ))'
    assert t('(∀ξ.p₁(ξ) ∨ q₁(ξ₀))') == '∀ξ₁.(p₁(ξ₁) ∨ q₁(ξ₀))'
    assert t('(∀ξ.p₁(ξ) ∨ ∀ξ.q₁(ξ))') == '∀ξ₀.∀ξ₁.(p₁(ξ₀) ∨ q₁(ξ₁))'
    assert t('((∃ξ.p₁(ξ) ∧ ∃η.q₁(η)) ∨ (∃ξ.p₁(ξ) ∧ ∃η.q₁(η)))') == '∃ξ₁.∃η₁.∃ξ₂.∃η₂.((p₁(ξ₁) ∧ q₁(η₁)) ∨ (p₁(ξ₂) ∧ q₁(η₂)))'
    assert t('((∀ξ.p₁(ξ) ∨ q₁(ξ)) ∧ ∃ξ₀.r₁(ξ₀))') == '∃ξ₁.∀ξ₂.((p₁(ξ₂) ∨ q₁(ξ)) ∧ r₁(ξ₁))'


def test_to_pnf(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> str:
        pnf = to_pnf(parse_formula(dummy_signature, string))
        assert is_formula_in_pnf(pnf)
        return str(pnf)

    assert t('(ξ = η)') == '(ξ = η)'
    assert t('¬∀η.p₁(ξ)') == '∃η.¬p₁(ξ)'
    assert t('((∀ξ.p₁(ξ) ∨ q₁(ξ)) ∧ ∃ξ.¬¬r₁(ξ))') == '∃ξ₀.∀ξ₁.((p₁(ξ₁) ∨ q₁(ξ)) ∧ r₁(ξ₀))'
    assert t('((∃ξ.¬p₁(ξ) → q₁(ξ)) ∧ ∃ξ.r₁(ξ₁))') == '∃ξ₀.∀ξ₂.((p₁(ξ₂) ∨ q₁(ξ)) ∧ r₁(ξ₁))'
