from ....support.pytest import pytest_parametrize_kwargs
from ..parsing import parse_untyped_term
from ..variables import get_bound_variables, get_open_variables
from .alpha import are_terms_alpha_equivalent, separate_free_and_bound_variables


@pytest_parametrize_kwargs(
    dict(m='x',      n='x'),
    dict(m='(xy)',   n='(xy)'),
    dict(m='(λx.x)', n='(λy.y)'),
    dict(
        m='(λx.(λy.(xy)))',
        n='(λa.(λb.(ab)))'
    ),
    dict(
        m='((λx.(λy.(xy)))x)',
        n='((λa.(λb.(ab)))x)'
    ),
)
def test_are_terms_alpha_equivalent_true(m: str, n: str) -> None:
    assert are_terms_alpha_equivalent(
        parse_untyped_term(m),
        parse_untyped_term(n)
    )


@pytest_parametrize_kwargs(
    dict(m='x',    n='y'),
    dict(m='(xy)', n='(xz)'),
    dict(
        m='(λx.(λy.(xy)))',
        n='(λa.(λa.(aa)))'
    ),
)
def test_are_terms_alpha_equivalent_false(m: str, n: str) -> None:
    assert not are_terms_alpha_equivalent(
        parse_untyped_term(m),
        parse_untyped_term(n)
    )


@pytest_parametrize_kwargs(
    # Cases where no renaming is needed
    dict(term='x',      expected='x'),
    dict(term='(xy)',   expected='(xy)'),
    dict(term='(λx.x)', expected='(λx.x)'),

    # Cases where renaming is needed
    dict(
        term=    '((λx.x)x)',
        expected='((λa.a)x)'
    ),
    dict(
        term=    '((λx.(xy))x)',
        expected='((λa.(ay))x)'
    ),
    dict(
        term=    '((λx.((λx.x)x))x)',
        expected='((λa.((λb.b)a))x)'
    ),
    dict(
        term=    '((λx.(λy.(xy)))(xy))',
        expected='((λa.(λb.(ab)))(xy))'
    ),

    # Verify that fresh variables don't shadow existing ones
    dict(
        term=    '((λa.(λx.(ax)))x)',
        expected='((λa.(λb.(ab)))x)'
    ),
)
def test_separate_free_and_bound_variables(term: str, expected: str) -> None:
    old_term = parse_untyped_term(term)
    new_term = separate_free_and_bound_variables(old_term)
    assert are_terms_alpha_equivalent(old_term, new_term)

    free = set(get_open_variables(new_term))
    bound = set(get_bound_variables(new_term))
    assert free.isdisjoint(bound)
    assert str(new_term) == expected
