from .parsing.parser import parse_formula
from .variables import get_free_variables


def test_get_free_variables() -> None:
    def t(string: str) -> set[str]:
        return set(map(str, get_free_variables(parse_formula(string))))

    assert t('(ξ = η)') == {'ξ', 'η'}
    assert t('(ξ₁ = η₂)') == {'ξ₁', 'η₂'}
    assert t('p(ξ, η)') == {'ξ', 'η'}
    assert t('∀η.p(ξ)') == {'ξ'}
    assert t('∀ξ.p(ξ)') == set()
    assert t('((∀η.p(η) ∨ q(ξ)) ∧ ∃η.r(η))') == {'ξ'}
