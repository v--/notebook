from .parsing import parse_formula
from .signature import FOLSignature
from .variables import get_free_variables


def test_get_free_variables(dummy_signature: FOLSignature) -> None:
    def t(string: str) -> set[str]:
        return set(map(str, get_free_variables(parse_formula(dummy_signature, string))))

    assert t('(x = y)') == {'x', 'y'}
    assert t('(x₁ = y₂)') == {'x₁', 'y₂'}
    assert t('P₂(x, y)') == {'x', 'y'}
    assert t('∀y.P₁(x)') == {'x'}
    assert t('∀x.P₁(x)') == set()
    assert t('((∀y.P₁(y) ∨ Q₁(x)) ∧ ∃y.R₁(y))') == {'x'}
