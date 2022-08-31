import pytest

from ..exceptions import NotebookCodeError
from .parser import parse_formula
from .pnf import is_formula_in_pnf, move_negations, move_quantifiers, remove_conditionals, to_pnf


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
        return str(move_negations(parse_formula(string)))

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

    assert t('(ξ = η)') == '(ξ = η)'
    assert t('∀η.p(ξ)') == '∀η.p(ξ)'
    assert t('∀η.∀η.p(ξ)') == '∀η.∀η.p(ξ)'
    assert t('∀η.∀η.p(η)') == '∀η.∀η.p(η)'
    assert t('(∀ξ.p(ξ) ∨ q(η))') == '∀ξ1.(p(ξ1) ∨ q(η))'
    assert t('(∀ξ.p(ξ) ∨ q(ξ))') == '∀ξ1.(p(ξ1) ∨ q(ξ))'
    assert t('(∀ξ.p(ξ) ∨ q(ξ1))') == '∀ξ2.(p(ξ2) ∨ q(ξ1))'
    assert t('(∀ξ.p(ξ) ∨ ∀ξ.q(ξ))') == '∀ξ1.∀ξ2.(p(ξ1) ∨ q(ξ2))'
    assert t('((∃ξ.p(ξ) ∧ ∃η.q(η)) ∨ (∃ξ.p(ξ) ∧ ∃η.q(η)))') == '∃ξ2.∃ξ3.∃η2.∃η3.((p(ξ2) ∧ q(η2)) ∨ (p(ξ3) ∧ q(η3)))'
    assert t('((∀ξ.p(ξ) ∨ q(ξ)) ∧ ∃ξ1.r(ξ1))') == '∃ξ2.∀ξ3.((p(ξ3) ∨ q(ξ)) ∧ r(ξ2))'


def test_to_pnf():
    def t(string: str):
        return str(to_pnf(parse_formula(string)))

    assert t('(ξ = η)') == '(ξ = η)'
    assert t('((∀ξ.p(ξ) ∨ q(ξ)) ∧ ∃ξ.¬¬r(ξ))') == '∃ξ1.∀ξ2.((p(ξ2) ∨ q(ξ)) ∧ r(ξ1))'
    assert t('((∃ξ.¬p(ξ) → q(ξ)) ∧ ∃ξ.r(ξ2))') == '∃ξ1.∀ξ3.((p(ξ3) ∨ q(ξ)) ∧ r(ξ2))'
