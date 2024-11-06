import functools
import inspect
from collections.abc import Callable

from ..modulo import Z2
from . import monomial
from .common import IRingPolynomial
from .monomial import Monomial


class ZhegalkinPolynomial(IRingPolynomial[Z2], semiring=Z2):
    pass


t, x, y, z = ZhegalkinPolynomial.from_monomials(monomial.const, monomial.x, monomial.y, monomial.z)
f = ZhegalkinPolynomial()


# This is alg:infer_zhegalkin_polynomial in the monograph
def infer_zhegalkin(fun: Callable[..., bool]) -> ZhegalkinPolynomial:
    fun_params = inspect.signature(fun).parameters

    for param in fun_params.values():
        assert all('a' <= c <= 'z' for c in param.name), \
            f'In order to become a valid variable name, the parameter name {param.name!r} must consist only of small Latin characters.'

    if len(fun_params) == 0:
        return t if fun() else f

    first_mon = next(Monomial.from_indeterminate(param.name) for param in fun_params.values())
    first_pol, = ZhegalkinPolynomial.from_monomials(first_mon)

    sub_t = infer_zhegalkin(functools.partial(fun, True))  # noqa: FBT003
    sub_f = infer_zhegalkin(functools.partial(fun, False))  # noqa: FBT003

    return first_pol * (sub_t + sub_f) + sub_f
