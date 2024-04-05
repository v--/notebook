from .parsing.parser import parse_formula
from .signature import FOLSignature
from .variables import get_free_variables


def test_get_free_variables(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> set[str]:
        return set(map(str, get_free_variables(parse_formula(dummy_signature, string))))

    assert t('(ξ = η)') == {'ξ', 'η'}
    assert t('(ξ₁ = η₂)') == {'ξ₁', 'η₂'}
    assert t('p₂(ξ, η)') == {'ξ', 'η'}
    assert t('∀η.p₁(ξ)') == {'ξ'}
    assert t('∀ξ.p₁(ξ)') == set()
    assert t('((∀η.p₁(η) ∨ q₁(ξ)) ∧ ∃η.r₁(η))') == {'ξ'}
