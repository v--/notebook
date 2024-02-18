from .alpha import are_terms_alpha_equivalent, disunify_free_bound_variables
from .parser import parse_term
from .variables import get_bound_variables, get_free_variables


def test_substitute_in_term():
    def t(m: str, n: str):
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


def test_disunify_free_bound_variables():
    def t(string: str):
        old_term = parse_term(string)
        new_term = disunify_free_bound_variables(old_term)
        assert are_terms_alpha_equivalent(old_term, new_term)
        assert get_free_variables(new_term).isdisjoint(get_bound_variables(new_term))
        return str(new_term)

    # Cases where no renaming is needed
    assert t('x') == 'x'
    assert t('(xy)') == '(xy)'
    assert t('(λx.x)') == '(λx.x)'

    # Cases where renaming is needed
    assert t('((λx.x)x)') == '((λx1.x1)x)'
    assert t('((λx.(xy))x)') == '((λx1.(x1y))x)'
    assert t('((λx.((λx.x)x))x)') == '((λx1.((λx2.x2)x1))x)'
    assert t('((λx.(λy.(xy)))(xy))') == '((λx1.(λy1.(x1y1)))(xy))'

    # Verify that new variables don't shadow existing ones
    assert t('((λx1.(λx.(x1x)))x)') == '((λx1.(λx2.(x1x2)))x)'
