from collections.abc import Collection
from typing import NamedTuple

from ....exceptions import UnreachableException
from ..types import IRing
from .common import IFieldPolynomial, IRingPolynomial
from .exceptions import PolynomialDivisionError
from .monomial import Monomial


def get_indeterminates[P: IRingPolynomial](pol: P) -> Collection[str]:
    indeterminates = set[str]()

    for mon in pol.get_monomials():
        for ind in mon.get_indeterminates():
            indeterminates.add(ind)

    return indeterminates


def is_univariate[P: IRingPolynomial](pol: P) -> bool:
    return len(get_indeterminates(pol)) <= 1


def leading_coefficient[N: IRing, P: IRingPolynomial](pol: P) -> N:
    assert is_univariate(pol)

    if pol.is_zero:
        return 0

    for mon in pol.get_monomials():
        if mon.total_degree == pol.total_degree:
            return pol[mon]

    raise UnreachableException


class DivMod[P: IRingPolynomial](NamedTuple):
    quot: P
    rem: P


# This is alg:euclidean_division_of_polynomials in the monograph
def pol_divmod[P: IRingPolynomial](f: P, g: P) -> DivMod:
    if g.is_zero:
        raise PolynomialDivisionError('Cannot divide by the zero polynomial')

    cls = type(f)

    zero = cls.new_zero()
    f_indets = get_indeterminates(f)
    g_indets = get_indeterminates(g)

    if f.is_zero and len(g_indets) <= 1:
        return DivMod(zero, zero)

    if len(f_indets) > 1 or len(g_indets) > 1 or f_indets != g_indets:
        raise PolynomialDivisionError(f'Expected univariate polynomials with a matching indeterminate, got {str(f)!r} and {str(g)!r}')

    if f.total_degree < g.total_degree:
        return DivMod(zero, f)

    f_lead = leading_coefficient(f)
    g_lead = leading_coefficient(g)

    if not isinstance(g, IFieldPolynomial) and g_lead != g.lift_to_scalar(1):
        raise PolynomialDivisionError(f'Expected either a polynomial over a field or a monic divisor, got {str(g)!r}')

    g_lead_inv = 1 / g_lead if isinstance(g, IFieldPolynomial) else 1

    if g.total_degree == 0:
        return DivMod(g_lead_inv * f, zero)

    indet = cls.from_monomial(Monomial.from_indeterminate(next(iter(g_indets))))

    leveling_term = (g_lead_inv * f_lead) * indet ** (f.total_degree - g.total_degree)
    r_ = f - leveling_term * g
    q_, r = pol_divmod(r_, g)
    q = q_ + leveling_term

    return DivMod(q, r)

