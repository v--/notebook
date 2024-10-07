from collections.abc import Mapping

from ....support.pytest import pytest_parametrize_kwargs
from . import common as var
from .polynomial import ZhegalkinPolynomial


@pytest_parametrize_kwargs(
    dict(
        result=var.F + var.x,
        expected=var.x
    ),
    dict(
        result=var.F * var.x,
        expected=var.F
    ),
    dict(
        result=var.T * var.x,
        expected=var.x
    ),
    dict(
        result=(var.x + var.T) * var.y,
        expected=var.y + var.x * var.y
    ),
    dict(
        result=var.x * (var.y + var.T),
        expected=var.x * var.y + var.x
    ),
    dict(
        result=var.x + var.x,
        expected=var.F
    ),
    dict(
        result=var.x * var.x,
        expected=var.F
    ),
    dict(
        result=var.x + var.y,
        expected=var.y + var.x
    ),
    dict(
        result=var.x + var.y + var.y,
        expected=var.x
    ),
    dict(
        result=var.x * var.y + var.y * var.x,
        expected=var.F
    )
)
def test_zhegalkin_operations(result: ZhegalkinPolynomial, expected: ZhegalkinPolynomial) -> None:
    assert result == expected


@pytest_parametrize_kwargs(
    dict(
        polynomial=var.F,
        params=dict(),
        expected=False
    ),
    dict(
        polynomial=var.T,
        params=dict(),
        expected=True
    ),
    dict(
        polynomial=var.x,
        params=dict(x=False),
        expected=False
    ),
    dict(
        polynomial=var.x,
        params=dict(x=True),
        expected=True
    ),
    dict(
        polynomial=var.x * var.y,
        params=dict(x=True, y=False),
        expected=False
    ),
    dict(
        polynomial=var.x * var.y,
        params=dict(x=True, y=True),
        expected=True
    )
)
def test_zhegalkin_eval(polynomial: ZhegalkinPolynomial, params: Mapping[str, bool], *, expected: bool) -> None:
    assert polynomial(**params) == expected
