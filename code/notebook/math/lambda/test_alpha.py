from .alpha import are_terms_alpha_equivalent, separate_free_and_bound_variables
from .parsing import parse_term
from .variables import get_bound_variables, get_free_variables


def test_substitute_in_term() -> None:
    def t(m: str, n: str) -> bool:
        return are_terms_alpha_equivalent(
            parse_term(m),
            parse_term(n)
        )

    assert t('x', 'x')
    assert t('(xy)', '(xy)')
    assert t('(λx.x)', '(λy.y)')
    assert t('(λx.(λy.(xy)))', '(λa.(λb.(ab)))')
    assert t('((λx.(λy.(xy)))x)', '((λa.(λb.(ab)))x)')

    assert not t('x', 'y')
    assert not t('(xy)', '(xz)')


def test_separate_free_and_bound_variables() -> None:
    def t(string: str) -> str:
        old_term = parse_term(string)
        new_term = separate_free_and_bound_variables(old_term)
        assert are_terms_alpha_equivalent(old_term, new_term)
        assert get_free_variables(new_term).isdisjoint(get_bound_variables(new_term))
        return str(new_term)

    # Cases where no renaming is needed
    assert t('x') == 'x'
    assert t('(xy)') == '(xy)'
    assert t('(λx.x)') == '(λx.x)'

    # Cases where renaming is needed
    assert t('((λx.x)x)') == '((λa.a)x)'
    assert t('((λx.(xy))x)') == '((λa.(ay))x)'
    assert t('((λx.((λx.x)x))x)') == '((λa.((λb.b)a))x)'
    assert t('((λx.(λy.(xy)))(xy))') == '((λa.(λb.(ab)))(xy))'

    # Verify that new variables don't shadow existing ones
    assert t('((λa.(λx.(ax)))x)') == '((λa.(λb.(ab)))x)'
