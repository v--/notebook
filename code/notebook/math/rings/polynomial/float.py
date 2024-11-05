from . import monomial
from .base import BasePolynomial, PolynomialSubtractionMixin


class FloatPolynomial(PolynomialSubtractionMixin[float], BasePolynomial[float], semiring=float):
    pass


const, x, y, z = FloatPolynomial.from_monomials(monomial.const, monomial.x, monomial.y, monomial.z)
zero = FloatPolynomial()
