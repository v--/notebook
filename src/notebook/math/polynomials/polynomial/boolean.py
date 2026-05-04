from notebook.math.polynomials import monomial
from notebook.math.rings.modular import Z2

from .common import IRingPolynomial


class BooleanPolynomial(IRingPolynomial[Z2], semiring=Z2):
    pass


true, x, y, z = BooleanPolynomial.from_monomials(monomial.const, monomial.x, monomial.y, monomial.z)
false = BooleanPolynomial()
