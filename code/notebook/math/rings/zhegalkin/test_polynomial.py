from collections.abc import Mapping

import pytest

from . import common as var
from .polynomial import ZhegalkinPolynomial


@pytest.mark.parametrize(
    ('result', 'expected'),
    [
        (var.F + var.x, var.x),
        (var.F * var.x, var.F),
        (var.T * var.x, var.x),
        ((var.x + var.T) * var.y, var.x + var.x * var.y),
        (var.x * (var.y + var.T), var.x * var.y + var.x),
        (var.x + var.x, var.F),
        (var.x * var.x, var.F),
        (var.x + var.y, var.y + var.x),
        (var.x + var.y + var.y, var.x),
        (var.x * var.y + var.y * var.x, var.F),
    ]
)
def test_zhegalkin_operations(result: ZhegalkinPolynomial, expected: ZhegalkinPolynomial) -> None:
    assert result == expected


@pytest.mark.parametrize(
    ('polynomial', 'params', 'expected'),
    [
        (var.F, {}, False),
        (var.T, {}, True),
        (var.x, {'x': False}, False),
        (var.x, {'x': True}, True),
        (var.x * var.y, {'x': True, 'y': False}, False),
        (var.x * var.y, {'x': True, 'y': True}, True)
    ]
)
def test_zhegalkin_eval(polynomial: ZhegalkinPolynomial, params: Mapping[str, bool], *, expected: bool) -> None:
    assert polynomial(**params) == expected
