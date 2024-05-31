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

    assert t('x', 'x', 'y') == 'y'
    assert t('y', 'x', 'z') == 'y'
    assert t('F₁(x)', 'x', 'y') == 'F₁(y)'
    assert t('F₂(G₁(x), H₁(G₁(x)))', 'G₁(x)', 'y') == 'F₂(y, H₁(y))'


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
    assert t('P₁(x)', 'x', 'y') == 'P₁(y)'
    assert t('P₁(y)', 'x', 'z') == 'P₁(y)'
    assert t('(G₁(x) = H₁(G₁(x)))', 'G₁(x)', 'y') == '(y = H₁(y))'
    assert t('((∃x.¬P₁(x) → ¬Q₁(x)) ∧ ∃x.R₁(z))', 'x', 'y') == '((∃x.¬P₁(x) → ¬Q₁(y)) ∧ ∃x.R₁(z))'

    # (Avoiding) capturing free variables
    assert t('∀x.P₁(y)', 'y', 'z') == '∀x.P₁(z)'
    assert t('∀x.P₁(y)', 'y', 'x') == '∀a.P₁(x)'
    assert t('∀x.P₂(x, y)', 'y', 'x') == '∀a.P₂(a, x)'

    # (Avoiding) colliding variables
    assert t('∀x.P₁(y)', 'y', 'x') == '∀a.P₁(x)'
