import functools
import inspect
from collections.abc import Callable

from ...parsing import LatinIdentifier
from ...support.unicode import Capitalization, is_latin_string
from .exceptions import IndeterminateError
from .monomial import Monomial
from .polynomial import BooleanPolynomial
from .polynomial import boolean as b


# This is alg:infer_zhegalkin_polynomial in the monograph
def infer_zhegalkin(fun: Callable[..., bool]) -> BooleanPolynomial:
    fun_params = inspect.signature(fun).parameters

    if len(fun_params) == 0:
        return b.true if fun() else b.false

    first_param = next(iter(fun_params.values()))

    if not is_latin_string(first_param.name, Capitalization.LOWER) or len(first_param.name) != 1:
        raise IndeterminateError(f'Expected a lowercase Latin letter as a parameter name, but got {first_param.name!r}.') from None

    first_pol, = BooleanPolynomial.from_monomials(Monomial.from_indeterminate(LatinIdentifier(first_param.name)))

    sub_t = infer_zhegalkin(functools.partial(fun, True))  # noqa: FBT003
    sub_f = infer_zhegalkin(functools.partial(fun, False))  # noqa: FBT003

    return first_pol * (sub_t + sub_f) + sub_f
