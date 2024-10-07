from collections.abc import Collection

from ...support.pytest import pytest_parametrize_kwargs
from .parsing import parse_term
from .variables import get_free_variables


@pytest_parametrize_kwargs(
    dict(term='x',           expected={'x'}),
    dict(term='(λx.x)',      expected=set()),
    dict(term='(λx.y)',      expected={'y'}),
    dict(term='(λx.(λy.z))', expected={'z'}),
    dict(term='(λx.(yz))',   expected={'y', 'z'}),
)
def test_get_free_variables(term: str, expected: Collection[str]) -> None:
    actual = set(map(str, get_free_variables(parse_term(term))))
    assert actual == expected
