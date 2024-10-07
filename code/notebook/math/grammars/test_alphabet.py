from collections.abc import Iterable

from ...support.pytest import pytest_parametrize_kwargs
from .alphabet import NonTerminal, new_non_terminal


@pytest_parametrize_kwargs(
    dict(
        base_name='test',
        context=[],
        expected='test₀'
    ),
    dict(
        base_name='test',
        context=['test₀'],
        expected='test₁'
    ),
    dict(
        base_name='test₀',
        context=[],
        expected='test₁'
    ),
)
def test_new_non_terminal(base_name: str, context: Iterable[str], expected: str) -> None:
    actual = new_non_terminal(base_name, set(map(NonTerminal, context)))
    assert actual.value == expected
