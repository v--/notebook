import pytest

from ..exceptions import NotebookCodeError
from .parser import parse_formula
from .pnf import is_formula_quantifierless, is_formula_in_pnf, remove_conditionals, push_negations, move_quantifiers, to_pnf


def test_is_formula_quantifierless():
    def t(string: str):
        return is_formula_quantifierless(parse_formula(string))

    assert t('⊤')
    assert t('(ξ = η)')
    assert t('((ξ = η) ∨ ¬(ξ = η))')
    assert not t('∀ξ.p(η)')
    assert not t('¬∀ξ.p(η)')


def test_is_formula_in_pnf():
    def t(string: str):
        return is_formula_in_pnf(parse_formula(string))

    assert t('(ξ = η)')
    assert t('∀ξ.p(η)')
    assert t('∀ζ.∃ζ.(¬r(η) ∧ ¬r(ζ, η))')
    assert not t('¬∀ξ.p(η)')
    assert not t('∀η.∃ζ.(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')


def test_remove_conditionals():
    def t(string: str):
        return str(remove_conditionals(parse_formula(string)))

    assert t('(ξ = η)') == '(ξ = η)'
    assert t('(p(ξ) ∨ q(η))') == '(p(ξ) ∨ q(η))'
    assert t('(p(ξ) → q(η))') == '(¬p(ξ) ∨ q(η))'
    assert t('(p(ξ) ↔ q(η))') == '((¬p(ξ) ∨ q(η)) ∧ (p(ξ) ∨ ¬q(η)))'
    assert t('¬(p(ξ) → q(η))') == '¬(¬p(ξ) ∨ q(η))'
    assert t('∀η.∃ζ.¬(p(ξ) → q(η))') == '∀η.∃ζ.¬(¬p(ξ) ∨ q(η))'


def test_move_negations():
    def t(string: str):
        return str(push_negations(parse_formula(string)))

    with pytest.raises(NotebookCodeError):
        t('¬(p(ξ) → p(η))')

    with pytest.raises(NotebookCodeError):
        t('¬(p(ξ) ↔ p(η))')

    assert t('(ξ = η)') == '(ξ = η)'
    assert t('¬(ξ = η)') == '¬(ξ = η)'
    assert t('¬¬(ξ = η)') == '(ξ = η)'
    assert t('¬(p(ξ) ∨ ¬q(η))') == '(¬p(ξ) ∧ q(η))'
    assert t('¬∀η.∃ζ.(p(ξ) ∨ ¬q(η))') == '∃η.∀ζ.(¬p(ξ) ∧ q(η))'
    assert t('¬(p(ξ) ∨ ¬(q(η) ∧ ¬(∃ζ.r(ζ) ∨ ¬s(τ))))') == '(¬p(ξ) ∧ (q(η) ∧ (∀ζ.¬r(ζ) ∧ s(τ))))'


def test_move_quantifiers():
    def t(string: str):
        return str(move_quantifiers(parse_formula(string)))

    with pytest.raises(NotebookCodeError):
        t('¬(p(ξ) → p(η))')

    with pytest.raises(NotebookCodeError):
        t('¬(p(ξ) ↔ p(η))')

    # It is expected not to work on formulas where negations are not moved inwards.
    assert t('¬∀η.p(ξ)') == '¬∀η.p(ξ)'

    assert t('(ξ = η)') == '(ξ = η)'
    assert t('∀η.p(ξ)') == '∀η.p(ξ)'
    assert t('∀η.∀η.p(ξ)') == '∀η.∀η.p(ξ)'
    assert t('∀η.∀η.p(η)') == '∀η.∀η.p(η)'
    assert t('(∀ξ.p(ξ) ∨ q(η))') == '∀ξ₀.(p(ξ₀) ∨ q(η))'
    assert t('(∀ξ.p(ξ) ∨ q(ξ))') == '∀ξ₀.(p(ξ₀) ∨ q(ξ))'
    assert t('(∀ξ.p(ξ) ∨ q(ξ₀))') == '∀ξ₁.(p(ξ₁) ∨ q(ξ₀))'
    assert t('(∀ξ.p(ξ) ∨ ∀ξ.q(ξ))') == '∀ξ₀.∀ξ₁.(p(ξ₀) ∨ q(ξ₁))'
    assert t('((∃ξ.p(ξ) ∧ ∃η.q(η)) ∨ (∃ξ.p(ξ) ∧ ∃η.q(η)))') == '∃ξ₁.∃η₁.∃ξ₂.∃η₂.((p(ξ₁) ∧ q(η₁)) ∨ (p(ξ₂) ∧ q(η₂)))'
    assert t('((∀ξ.p(ξ) ∨ q(ξ)) ∧ ∃ξ₀.r(ξ₀))') == '∃ξ₁.∀ξ₂.((p(ξ₂) ∨ q(ξ)) ∧ r(ξ₁))'


def test_to_pnf():
    def t(string: str):
        pnf = to_pnf(parse_formula(string))
        assert is_formula_in_pnf(pnf)
        return str(pnf)

    assert t('(ξ = η)') == '(ξ = η)'
    assert t('¬∀η.p(ξ)') == '∃η.¬p(ξ)'
    assert t('((∀ξ.p(ξ) ∨ q(ξ)) ∧ ∃ξ.¬¬r(ξ))') == '∃ξ₀.∀ξ₁.((p(ξ₁) ∨ q(ξ)) ∧ r(ξ₀))'
    assert t('((∃ξ.¬p(ξ) → q(ξ)) ∧ ∃ξ.r(ξ₁))') == '∃ξ₀.∀ξ₂.((p(ξ₂) ∨ q(ξ)) ∧ r(ξ₁))'
