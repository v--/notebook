from .parsing.parser import parse_formula, parse_term
from .substitution import substitute_in_formula, substitute_in_term


def test_substitute_in_term() -> None:
    def t(term: str, from_term: str, to_term: str) -> str:
        return str(
            substitute_in_term(
                parse_term(term),
                parse_term(from_term),
                parse_term(to_term)
            )
        )

    assert t('ξ', 'ξ', 'η') == 'η'
    assert t('η', 'ξ', 'ζ') == 'η'
    assert t('f(ξ)', 'ξ', 'η') == 'f(η)'
    assert t('f(g(ξ), h(g(ξ)))', 'g(ξ)', 'η') == 'f(η, h(η))'


def test_substitute_in_formula() -> None:
    def t(formula: str, from_term: str, to_term: str) -> str:
        return str(
            substitute_in_formula(
                parse_formula(formula),
                parse_term(from_term),
                parse_term(to_term)
            )
        )

    # Straighforward substitution
    assert t('p(ξ)', 'ξ', 'η') == 'p(η)'
    assert t('p(η)', 'ξ', 'ζ') == 'p(η)'
    assert t('(g(ξ) = h(g(ξ)))', 'g(ξ)', 'η') == '(η = h(η))'
    assert t('((∃ξ.¬p(ξ) → ¬q(ξ)) ∧ ∃ξ.r(ζ))', 'ξ', 'η') == '((∃ξ.¬p(ξ) → ¬q(η)) ∧ ∃ξ.r(ζ))'

    # (Avoiding) capturing free variables
    assert t('∀ξ.p(η)', 'η', 'ζ') == '∀ξ.p(ζ)'
    assert t('∀ξ.p(η)', 'η', 'ξ') == '∀ξ₀.p(ξ)'
    assert t('∀ξ.p(ξ, η)', 'η', 'ξ') == '∀ξ₀.p(ξ₀, ξ)'

    # (Avoiding) colliding variables
    assert t('∀ξ.p(η)', 'η', 'ξ') == '∀ξ₀.p(ξ)'
