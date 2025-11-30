from ...rings.modular import Z2
from .. import monomial
from .common import IRingPolynomial


class ZhegalkinPolynomial(IRingPolynomial[Z2], semiring=Z2):
    pass


t, x, y, z = ZhegalkinPolynomial.from_monomials(monomial.const, monomial.x, monomial.y, monomial.z)
f = ZhegalkinPolynomial()
