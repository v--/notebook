from typing import NamedTuple

from ...parsing import LatinIdentifier
from ..rings.types import IRing
from . import monomial
from .exceptions import PolynomialDivisionError, ZeroPolynomialError
from .monomial import Monomial
from .polynomial import IFieldPolynomial, IRingPolynomial, ISemiringPolynomial


class DivMod[P: ISemiringPolynomial](NamedTuple):
    quot: P
    rem: P


# This is alg:euclidean_division_of_polynomials in the monograph
def euclidean_divmod[P: IRingPolynomial](f: P, g: P, indet: LatinIdentifier) -> DivMod[P]:
    f_deg = f.get_degree(indet)
    g_deg = g.get_degree(indet)

    if g_deg.is_undefined:
        raise ZeroPolynomialError('Cannot divide by the zero polynomial')

    cls = type(f)
    zero = cls.new_zero()

    if f_deg < g_deg:
        return DivMod(zero, f)

    scalar_one = cls.lift_to_scalar(1)
    f_lead = f.leading_coefficient(indet)
    g_lead = g.leading_coefficient(indet)

    if not isinstance(g, IFieldPolynomial) and g_lead != cls.lift(scalar_one):
        raise PolynomialDivisionError('Over rings more general than fields, we cannot determine whether the leading coefficient of a polynomial is invertible, so we require the polynomial to be monic')

    g_lead_inv = scalar_one / g_lead if isinstance(g, IFieldPolynomial) else scalar_one
    indet_pol = cls.from_monomial(Monomial.from_indeterminate(indet))
    leveling_term = (g_lead_inv * f_lead) * indet_pol ** int(f_deg - g_deg)
    r_ = f - leveling_term * g
    q_, r = euclidean_divmod(r_, g, indet)
    q = q_ + leveling_term

    return DivMod(q, r)


# This is alg:horners_rule in the monograph
def horner_divmod[N: IRing, P: IRingPolynomial](f: P, indet: LatinIdentifier, free: N) -> DivMod[P]:
    cls = type(f)

    if f.is_zero:
        zero = cls.new_zero()
        return DivMod(zero, zero)

    quot = cls.new_zero()
    rem = cls.new_zero()
    mon = Monomial.from_indeterminate(indet)
    degree = int(f.get_degree(indet))

    for k in range(1, degree + 1):
        quot[mon ** (degree - k)] = f[mon ** (degree - (k - 1))] - free * quot[mon ** (degree - (k - 1))]

    rem[monomial.const] = f[monomial.const] - free * quot[monomial.const]
    return DivMod(quot, rem)
