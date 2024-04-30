from .parsing import parse_term
from .variables import get_free_variables


def test_get_free_variables() -> None:
    def t(string: str) -> set[str]:
        return set(map(str, get_free_variables(parse_term(string))))

    assert t('x') == {'x'}
    assert t('(λx.x)') == set()
    assert t('(λx.y)') == {'y'}
    assert t('(λx.(λy.z))') == {'z'}
    assert t('(λx.(yz))') == {'y', 'z'}
