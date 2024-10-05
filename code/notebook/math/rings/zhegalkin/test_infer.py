from collections.abc import Callable

import pytest

from . import common as var
from .infer import infer_zhegalkin
from .polynomial import ZhegalkinPolynomial


@pytest.mark.parametrize(
    ('predicate', 'polynomial'),
    [
        (
            lambda: True,
            var.T
        ),

        (
            lambda: False,
            var.F
        ),

        (
            lambda x: False,  # noqa: ARG005
            var.F
        ),

        (
            lambda x: x,
            var.x
        ),

        (
            lambda x: not x,
            var.x + var.T
        ),

        (
            lambda x, y: x or y,
            var.x * var.y + var.x + var.y
        ),

        (
            lambda x, y: x and y,
            var.x * var.y
        ),

        (
            lambda x, y: (not x) or y,
            var.x * var.y + var.x + var.T
        ),

        (
            lambda x, y: (x and y) or (not x and not y),
            var.x + var.y + var.T
        ),
    ]
)
def test_infer_zhegalkin(predicate: Callable[..., bool], polynomial: ZhegalkinPolynomial) -> None:
    assert infer_zhegalkin(predicate) == polynomial
