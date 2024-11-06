from . import monomial
from .common import IRingPolynomial


class IntPolynomial(IRingPolynomial[int], semiring=int):
    pass


const, x, y, z = IntPolynomial.from_monomials(monomial.const, monomial.x, monomial.y, monomial.z)
zero = IntPolynomial()
