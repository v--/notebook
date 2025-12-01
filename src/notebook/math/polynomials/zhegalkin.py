import functools
import inspect
from collections.abc import Callable

from .monomial import Monomial
from .polynomial import BooleanPolynomial
from .polynomial import boolean as b


# This is alg:infer_zhegalkin_polynomial in the monograph
def infer_zhegalkin(fun: Callable[..., bool]) -> BooleanPolynomial:
    fun_params = inspect.signature(fun).parameters

    if len(fun_params) == 0:
        return b.true if fun() else b.false

    first_mon = next(Monomial.from_indeterminate(param.name) for param in fun_params.values())
    first_pol, = BooleanPolynomial.from_monomials(first_mon)

    sub_t = infer_zhegalkin(functools.partial(fun, True))  # noqa: FBT003
    sub_f = infer_zhegalkin(functools.partial(fun, False))  # noqa: FBT003

    return first_pol * (sub_t + sub_f) + sub_f
