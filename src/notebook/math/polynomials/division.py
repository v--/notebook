from typing import NamedTuple

from ..rings.types import IRing, ISemiring
from . import monomial
from .exceptions import PolynomialDivisionError, PolynomialZeroDivisionError
from .monomial import Monomial
from .polynomial import IFieldPolynomial, IRingPolynomial, ISemiringPolynomial


def get_degree_of[N: ISemiring, P: ISemiringPolynomial](pol: P, indet: str) -> int:
    assert not pol.is_zero
    max_degree = 0

    for mon in pol.get_monomials():
        if indet in mon.get_indeterminates() and mon[indet] > max_degree:
            max_degree = mon[indet]

    return max_degree


def leading_coefficient[N: ISemiring, P: ISemiringPolynomial](pol: P, indet: str) -> P:
    result = pol.new_zero()

    if pol.is_zero:
        return result

    max_degree = get_degree_of(pol, indet)

    for mon in pol.get_monomials():
        if mon[indet] == max_degree:
            new_mon = Monomial(**{ind: mon[ind] for ind in mon if ind != indet})
            result[new_mon] = pol[mon]

    if result.is_zero:
        result[monomial.const] = pol[monomial.const]

    return result


class DivMod[P: ISemiringPolynomial](NamedTuple):
    quot: P
    rem: P


# This is alg:euclidean_division_of_polynomials in the monograph
def euclidean_divmod[P: IRingPolynomial](f: P, g: P, indet: str) -> DivMod[P]:
    if g.is_zero:
        raise PolynomialZeroDivisionError('Cannot divide by the zero polynomial')

    cls = type(f)
    zero = cls.new_zero()
    scalar_one = cls.lift_to_scalar(1)

    if f.is_zero:
        return DivMod(zero, zero)

    f_deg = get_degree_of(f, indet)
    g_deg = get_degree_of(g, indet)

    if f_deg < g_deg:
        return DivMod(zero, f)

    f_lead = leading_coefficient(f, indet)
    g_lead = leading_coefficient(g, indet)

    if not isinstance(g, IFieldPolynomial) and g_lead != cls.lift(1):
        raise PolynomialDivisionError(f'Expected either polynomials over a field or a monic divisor, got {str(g)!r}')

    g_lead_inv = scalar_one / g_lead if isinstance(g, IFieldPolynomial) else scalar_one
    indet_pol = cls.from_monomial(Monomial.from_indeterminate(indet))
    leveling_term = (g_lead_inv * f_lead) * indet_pol ** (f_deg - g_deg)
    r_ = f - leveling_term * g
    q_, r = euclidean_divmod(r_, g, indet)
    q = q_ + leveling_term

    return DivMod(q, r)


# This is alg:horners_rule in the monograph
def horner_divmod[N: IRing, P: IRingPolynomial](pol: P, indet: str, free: N) -> DivMod[P]:
    cls = type(pol)

    if pol.is_zero:
        zero = cls.new_zero()
        return DivMod(zero, zero)

    quot = cls.new_zero()
    rem = cls.new_zero()
    mon = Monomial.from_indeterminate(indet)
    degree = get_degree_of(pol, indet)

    for k in range(1, degree + 1):
        quot[mon ** (degree - k)] = pol[mon ** (degree - (k - 1))] - free * quot[mon ** (degree - (k - 1))]

    rem[monomial.const] = pol[monomial.const] - free * quot[monomial.const]
    return DivMod(quot, rem)
