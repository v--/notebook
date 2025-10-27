import functools
import inspect
from collections.abc import Callable

from .monomial import Monomial
from .polynomial import ZhegalkinPolynomial
from .polynomial import zhegalkin as z


# This is alg:infer_zhegalkin_polynomial in the monograph
def infer_zhegalkin(fun: Callable[..., bool]) -> ZhegalkinPolynomial:
    fun_params = inspect.signature(fun).parameters

    for param in fun_params.values():
        assert all('a' <= c <= 'z' for c in param.name), \
            f'In order to become a valid variable name, the parameter name {param.name!r} must consist only of small Latin characters.'

    if len(fun_params) == 0:
        return z.t if fun() else z.f

    first_mon = next(Monomial.from_indeterminate(param.name) for param in fun_params.values())
    first_pol, = ZhegalkinPolynomial.from_monomials(first_mon)

    sub_t = infer_zhegalkin(functools.partial(fun, True))  # noqa: FBT003
    sub_f = infer_zhegalkin(functools.partial(fun, False))  # noqa: FBT003

    return first_pol * (sub_t + sub_f) + sub_f
