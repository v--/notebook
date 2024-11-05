from . import monomial
from .base import BasePolynomial, PolynomialSubtractionMixin


class IntPolynomial(PolynomialSubtractionMixin[int], BasePolynomial[int], semiring=int):
    pass


const, x, y, z = IntPolynomial.from_monomials(monomial.const, monomial.x, monomial.y, monomial.z)
zero = IntPolynomial()
