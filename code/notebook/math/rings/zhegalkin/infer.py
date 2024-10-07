import functools
import inspect
from collections.abc import Callable

from . import common as var
from .polynomial import ZhegalkinPolynomial


# This is alg:infer_zhegalkin_polynomial in the monograph
def infer_zhegalkin(fun: Callable[..., bool]) -> ZhegalkinPolynomial:
    fun_params = inspect.signature(fun).parameters

    for param in fun_params.values():
        assert all('a' <= c <= 'z' for c in param.name), \
            f'In order to become a valid variable name, the parameter name {param.name!r} must consist only of small Latin characters.'

    if len(fun_params) == 0:
        return var.T if fun() else var.F

    first = next(param.name for param in fun_params.values())
    first_var = ZhegalkinPolynomial(payload=[frozenset(first)], free=False)

    sub_t = infer_zhegalkin(functools.partial(fun, True))  # noqa: FBT003
    sub_f = infer_zhegalkin(functools.partial(fun, False))  # noqa: FBT003

    return first_var * (sub_t + sub_f) + sub_f
