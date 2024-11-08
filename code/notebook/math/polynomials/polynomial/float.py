from .. import monomial
from .common import IRingPolynomial


class FloatPolynomial(IRingPolynomial[float], semiring=float):
    pass


const, x, y, z = FloatPolynomial.from_monomials(monomial.const, monomial.x, monomial.y, monomial.z)
zero = FloatPolynomial()
