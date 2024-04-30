from .parsing import parse_formula, parse_term
from .signature import FOLSignature
from .substitution import substitute_in_formula, substitute_in_term


def test_substitute_in_term(dummy_signature: FOLSignature) -> None:
    def t(term: str, from_term: str, to_term: str) -> str:
        return str(
            substitute_in_term(
                parse_term(dummy_signature, term),
                parse_term(dummy_signature, from_term),
                parse_term(dummy_signature, to_term)
            )
        )

    assert t('ξ', 'ξ', 'η') == 'η'
    assert t('η', 'ξ', 'ζ') == 'η'
    assert t('f₁(ξ)', 'ξ', 'η') == 'f₁(η)'
    assert t('f₂(g₁(ξ), h₁(g₁(ξ)))', 'g₁(ξ)', 'η') == 'f₂(η, h₁(η))'


def test_substitute_in_formula(dummy_signature: FOLSignature) -> None:
    def t(formula: str, from_term: str, to_term: str) -> str:
        return str(
            substitute_in_formula(
                parse_formula(dummy_signature, formula),
                parse_term(dummy_signature, from_term),
                parse_term(dummy_signature, to_term)
            )
        )

    # Straighforward substitution
    assert t('p₁(ξ)', 'ξ', 'η') == 'p₁(η)'
    assert t('p₁(η)', 'ξ', 'ζ') == 'p₁(η)'
    assert t('(g₁(ξ) = h₁(g₁(ξ)))', 'g₁(ξ)', 'η') == '(η = h₁(η))'
    assert t('((∃ξ.¬p₁(ξ) → ¬q₁(ξ)) ∧ ∃ξ.r₁(ζ))', 'ξ', 'η') == '((∃ξ.¬p₁(ξ) → ¬q₁(η)) ∧ ∃ξ.r₁(ζ))'

    # (Avoiding) capturing free variables
    assert t('∀ξ.p₁(η)', 'η', 'ζ') == '∀ξ.p₁(ζ)'
    assert t('∀ξ.p₁(η)', 'η', 'ξ') == '∀ξ₀.p₁(ξ)'
    assert t('∀ξ.p₂(ξ, η)', 'η', 'ξ') == '∀ξ₀.p₂(ξ₀, ξ)'

    # (Avoiding) colliding variables
    assert t('∀ξ.p₁(η)', 'η', 'ξ') == '∀ξ₀.p₁(ξ)'
