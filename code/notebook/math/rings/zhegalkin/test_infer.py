from collections.abc import Callable

from ....support.pytest import pytest_parametrize_kwargs
from . import common as var
from .infer import infer_zhegalkin
from .polynomial import ZhegalkinPolynomial


@pytest_parametrize_kwargs(
    dict(
        predicate=lambda: True,
        polynomial=var.T
    ),

    dict(
        predicate=lambda: False,
        polynomial=var.F
    ),

    dict(
        predicate=lambda x: False,  # noqa: ARG005
        polynomial=var.F
    ),

    dict(
        predicate=lambda x: x,
        polynomial=var.x
    ),

    dict(
        predicate=lambda x: not x,
        polynomial=var.x + var.T
    ),

    dict(
        predicate=lambda x, y: x or y,
        polynomial=var.x * var.y + var.x + var.y
    ),

    dict(
        predicate=lambda x, y: x and y,
        polynomial=var.x * var.y
    ),

    dict(
        predicate=lambda x, y: (not x) or y,
        polynomial=var.x * var.y + var.x + var.T
    ),

    dict(
        predicate=lambda x, y: (x and y) or (not x and not y),
        polynomial=var.x + var.y + var.T
    )
)
def test_infer_zhegalkin(predicate: Callable[..., bool], polynomial: ZhegalkinPolynomial) -> None:
    assert infer_zhegalkin(predicate) == polynomial
