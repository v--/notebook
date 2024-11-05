from collections.abc import Callable

from ....support.pytest import pytest_parametrize_kwargs
from . import zhegalkin as z
from .zhegalkin import ZhegalkinPolynomial, infer_zhegalkin


@pytest_parametrize_kwargs(
    dict(
        predicate=lambda: True,
        polynomial=z.t
    ),

    dict(
        predicate=lambda: False,
        polynomial=z.f
    ),

    dict(
        predicate=lambda x: False,  # noqa: ARG005
        polynomial=z.f
    ),

    dict(
        predicate=lambda x: x,
        polynomial=z.x
    ),

    dict(
        predicate=lambda x: not x,
        polynomial=z.x + z.t
    ),

    dict(
        predicate=lambda x, y: x or y,
        polynomial=z.x * z.y + z.x + z.y
    ),

    dict(
        predicate=lambda x, y: x and y,
        polynomial=z.x * z.y
    ),

    dict(
        predicate=lambda x, y: (not x) or y,
        polynomial=z.x * z.y + z.x + z.t
    ),

    dict(
        predicate=lambda x, y: (x and y) or (not x and not y),
        polynomial=z.x + z.y + z.t
    )
)
def test_infer_zhegalkin(predicate: Callable[..., bool], polynomial: ZhegalkinPolynomial) -> None:
    assert infer_zhegalkin(predicate) == polynomial
