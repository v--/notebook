from typing import TYPE_CHECKING

from .name_collision import get_name_without_collision
from .pytest import pytest_parametrize_kwargs


if TYPE_CHECKING:
    from collections.abc import Collection


@pytest_parametrize_kwargs(
    dict(
        base_name='test',
        context=set(),
        expected='test',
    ),
    dict(
        base_name='test',
        context={'test', 'test₁'},
        expected='test₂',
    ),
    dict(
        base_name='test₋₁',
        context={'test₋₁'},
        expected='test₀',
    ),
    dict(
        base_name='test₀',
        context={'test₀'},
        expected='test₁',
    ),
    dict(
        base_name='test₁',
        context={'test₁'},
        expected='test₂',
    ),
)
def test_get_name_without_collision(base_name: str, context: Collection[str], expected: str) -> None:
    actual = get_name_without_collision(base_name, context)
    assert actual == expected
