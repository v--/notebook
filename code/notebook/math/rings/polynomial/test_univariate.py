import pytest

from ....support.pytest import pytest_parametrize_kwargs
from .exceptions import PolynomialDivisionError
from .int import IntPolynomial, const, x, y, zero
from .univariate import DivMod, pol_divmod


@pytest_parametrize_kwargs(
    dict(f=zero,                       g=const,      q=zero,              r=zero             ),
    dict(f=const,                      g=const,      q=const,             r=zero             ),
    dict(f=x ** 2,                     g=x,          q=x,                 r=zero             ),
    dict(f=x ** 2 - const,             g=x - const,  q=x + const,         r=zero             ),
    dict(f=3 * x ** 3 + x + 2 * const, g=x ** 2 - x, q=3 * x + 3 * const, r=4 * x + 2 * const),
)
def test_pol_divmod(f: IntPolynomial, g: IntPolynomial, q: IntPolynomial, r: IntPolynomial) -> None:
    assert pol_divmod(f, g) == DivMod(q, r)


def test_pol_divmod_failure_division_by_zero() -> None:
    with pytest.raises(PolynomialDivisionError, match='Cannot divide by the zero polynomial'):
        pol_divmod(x, zero)


def test_pol_divmod_failure_non_monic() -> None:
    with pytest.raises(PolynomialDivisionError, match="Expected either a polynomial over a field or a monic divisor, got '2x'"):
        pol_divmod(x, 2 * x)


def test_pol_divmod_failure_multivariate() -> None:
    with pytest.raises(PolynomialDivisionError, match="Expected univariate polynomials with a matching indeterminate, got 'xy' and 'x'"):
        pol_divmod(x * y, x)


def test_pol_divmod_failure_indeterminate_mismatch() -> None:
    with pytest.raises(PolynomialDivisionError, match="Expected univariate polynomials with a matching indeterminate, got 'x' and 'y'"):
        pol_divmod(x, y)
