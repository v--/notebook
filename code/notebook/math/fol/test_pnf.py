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
    assert t('(x = y)')
    assert t('((x = y) ∨ ¬(x = y))')
    assert not t('∀x.P₁(y)')
    assert not t('¬∀x.P₁(y)')


def test_is_formula_in_pnf(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> bool:
        return is_formula_in_pnf(parse_formula(dummy_signature, string))

    assert t('(x = y)')
    assert t('∀x.P₁(y)')
    assert t('∀z.∃z.(¬R₁(y) ∧ ¬R₂(z, y))')
    assert not t('¬∀x.P₁(y)')
    assert not t('∀y.∃z.(¬P₁(z) ∧ ∀x.(Q₂(z, x) → ¬R₂(y, x)))')


def test_remove_conditionals(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> str:
        return str(remove_conditionals(parse_formula(dummy_signature, string)))

    assert t('(x = y)') == '(x = y)'
    assert t('(P₁(x) ∨ Q₁(y))') == '(P₁(x) ∨ Q₁(y))'
    assert t('(P₁(x) → Q₁(y))') == '(¬P₁(x) ∨ Q₁(y))'
    assert t('(P₁(x) ↔ Q₁(y))') == '((¬P₁(x) ∨ Q₁(y)) ∧ (P₁(x) ∨ ¬Q₁(y)))'
    assert t('¬(P₁(x) → Q₁(y))') == '¬(¬P₁(x) ∨ Q₁(y))'
    assert t('∀y.∃z.¬(P₁(x) → Q₁(y))') == '∀y.∃z.¬(¬P₁(x) ∨ Q₁(y))'


def test_move_negations(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> str:
        return str(push_negations(parse_formula(dummy_signature, string)))

    with pytest.raises(PNFError):
        t('¬(P₁(x) → P₁(y))')

    with pytest.raises(PNFError):
        t('¬(P₁(x) ↔ P₁(y))')

    assert t('(x = y)') == '(x = y)'
    assert t('¬(x = y)') == '¬(x = y)'
    assert t('¬¬(x = y)') == '(x = y)'
    assert t('¬(P₁(x) ∨ ¬Q₁(y))') == '(¬P₁(x) ∧ Q₁(y))'
    assert t('¬∀y.∃z.(P₁(x) ∨ ¬Q₁(y))') == '∃y.∀z.(¬P₁(x) ∧ Q₁(y))'
    assert t('¬(P₁(x) ∨ ¬(Q₁(y) ∧ ¬(∃z.R₁(z) ∨ ¬S₀)))') == '(¬P₁(x) ∧ (Q₁(y) ∧ (∀z.¬R₁(z) ∧ S₀)))'


def test_move_quantifiers(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> str:
        return str(move_quantifiers(parse_formula(dummy_signature, string)))

    with pytest.raises(PNFError):
        t('¬(P₁(x) → P₁(y))')

    with pytest.raises(PNFError):
        t('¬(P₁(x) ↔ P₁(y))')

    # It is expected not to work on formulas where negations are not moved inwards.
    assert t('¬∀y.P₁(x)') == '¬∀y.P₁(x)'

    assert t('(x = y)') == '(x = y)'
    assert t('∀y.P₁(x)') == '∀y.P₁(x)'
    assert t('∀y.∀y.P₁(x)') == '∀y.∀y.P₁(x)'
    assert t('∀y.∀y.P₁(y)') == '∀y.∀y.P₁(y)'
    assert t('(∀x.P₁(x) ∨ Q₁(y))') == '∀a.(P₁(a) ∨ Q₁(y))'
    assert t('(∀x.P₁(x) ∨ Q₁(x))') == '∀a.(P₁(a) ∨ Q₁(x))'
    assert t('(∀x.P₁(x) ∨ Q₁(a))') == '∀b.(P₁(b) ∨ Q₁(a))'
    assert t('(∀x.P₁(x) ∨ ∀x.Q₁(x))') == '∀a.∀b.(P₁(a) ∨ Q₁(b))'
    assert t('((∃x.P₁(x) ∧ ∃y.Q₁(y)) ∨ (∃x.P₁(x) ∧ ∃y.Q₁(y)))') == '∃b.∃a.∃c.∃d.((P₁(b) ∧ Q₁(a)) ∨ (P₁(c) ∧ Q₁(d)))'
    assert t('((∀x.P₁(x) ∨ Q₁(x)) ∧ ∃a.R₁(a))') == '∃b.∀c.((P₁(c) ∨ Q₁(x)) ∧ R₁(b))'


def test_to_pnf(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> str:
        pnf = to_pnf(parse_formula(dummy_signature, string))
        assert is_formula_in_pnf(pnf)
        return str(pnf)

    assert t('(x = y)') == '(x = y)'
    assert t('¬∀y.P₁(x)') == '∃y.¬P₁(x)'
    assert t('((∀x.P₁(x) ∨ Q₁(x)) ∧ ∃x.¬¬R₁(x))') == '∃a.∀b.((P₁(b) ∨ Q₁(x)) ∧ R₁(a))'
    assert t('((∃x.¬P₁(x) → Q₁(x)) ∧ ∃x.R₁(b))') == '∃a.∀c.((P₁(c) ∨ Q₁(x)) ∧ R₁(b))'
