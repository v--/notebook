import pytest

from ...parsing import LatinIdentifier
from ...parsing import common_identifiers as ci
from ...support.pytest import pytest_parametrize_kwargs
from ..rings.modular import Z4
from . import monomial as mon
from .division import DivMod, euclidean_divmod, horner_divmod
from .exceptions import PolynomialDivisionError, ZeroPolynomialError
from .polynomial.common import IRingPolynomial
from .polynomial.int import IntPolynomial, const, x, y, z, zero


@pytest_parametrize_kwargs(
    dict(f=zero,                       g=const,      indet=ci.x, q=zero,                  r=zero             ),
    dict(f=const,                      g=const,      indet=ci.x, q=const,                 r=zero             ),
    dict(f=x ** 2,                     g=x,          indet=ci.x, q=x,                     r=zero             ),
    dict(f=x ** 2 - const,             g=x - const,  indet=ci.x, q=x + const,             r=zero             ),
    dict(f=3 * x ** 3 + x + 2 * const, g=x ** 2 - x, indet=ci.x, q=3 * x + 3 * const,     r=4 * x + 2 * const),
    dict(f=x ** 2 * y + x * z + 2 * x, g=x,          indet=ci.x, q=x * y + z + 2 * const, r=zero             ),
)
def test_euclidean_divmod(f: IntPolynomial, g: IntPolynomial, indet: LatinIdentifier, q: IntPolynomial, r: IntPolynomial) -> None:
    assert euclidean_divmod(f, g, indet) == DivMod(q, r)


def test_euclidean_divmod_failure_division_by_zero() -> None:
    with pytest.raises(ZeroPolynomialError, match='Cannot divide by the zero polynomial'):
        euclidean_divmod(x, zero, ci.x)


class Z4Polynomial(IRingPolynomial, semiring=Z4):
    pass


z4x = Z4Polynomial.from_monomial(mon.x)


def test_euclidean_divmod_failure_non_invertible() -> None:
    with pytest.raises(PolynomialDivisionError, match='Over rings more general than fields, we cannot determine whether the leading coefficient of a polynomial is invertible, so we require the polynomial to be monic'):
        euclidean_divmod(z4x ** 2, 2 * z4x, ci.x)


@pytest_parametrize_kwargs(
    dict(pol=zero,                       free=0, indet=ci.x),
    dict(pol=const,                      free=0, indet=ci.x),
    dict(pol=const,                      free=1, indet=ci.x),
    dict(pol=x ** 2,                     free=0, indet=ci.x),
    dict(pol=x ** 2,                     free=1, indet=ci.x),
    dict(pol=3 * x ** 3 + x + 2 * const, free=3, indet=ci.x),
)
def test_horner_divmod(pol: IntPolynomial, free: int, indet: LatinIdentifier) -> None:
    g = IntPolynomial.lift(free)
    g[mon.Monomial.from_indeterminate(indet)] = 1
    assert horner_divmod(pol, indet, free) == euclidean_divmod(pol, g, indet)
