from collections.abc import Callable

from ...support.pytest import pytest_parametrize_kwargs
from .polynomial import BooleanPolynomial
from .polynomial import boolean as b
from .zhegalkin import infer_zhegalkin


@pytest_parametrize_kwargs(
    dict(
        predicate=lambda: True,
        polynomial=b.true
    ),

    dict(
        predicate=lambda: False,
        polynomial=b.false
    ),

    dict(
        predicate=lambda x: False,  # noqa: ARG005
        polynomial=b.false
    ),

    dict(
        predicate=lambda x: x,
        polynomial=b.x
    ),

    dict(
        predicate=lambda x: not x,
        polynomial=b.x + b.true
    ),

    dict(
        predicate=lambda x, y: x or y,
        polynomial=b.x * b.y + b.x + b.y
    ),

    dict(
        predicate=lambda x, y: x and y,
        polynomial=b.x * b.y
    ),

    dict(
        predicate=lambda x, y: (not x) or y,
        polynomial=b.x * b.y + b.x + b.true
    ),

    dict(
        predicate=lambda x, y: (x and y) or (not x and not y),
        polynomial=b.x + b.y + b.true
    )
)
def test_infer_zhegalkin(predicate: Callable[..., bool], polynomial: BooleanPolynomial) -> None:
    assert infer_zhegalkin(predicate) == polynomial
