
from typing import TYPE_CHECKING

from ...support.pytest import pytest_parametrize_kwargs
from .parsing import parse_untyped_term
from .variables import get_free_variables


if TYPE_CHECKING:
    from collections.abc import Collection


@pytest_parametrize_kwargs(
    dict(term='x',           expected={'x'}),
    dict(term='(λx.x)',      expected=set()),
    dict(term='(λx.y)',      expected={'y'}),
    dict(term='(λx.(λy.z))', expected={'z'}),
    dict(term='(λx.(yz))',   expected={'y', 'z'}),
)
def test_get_open_variables(term: str, expected: Collection[str]) -> None:
    actual = set(map(str, get_free_variables(parse_untyped_term(term))))
    assert actual == expected
