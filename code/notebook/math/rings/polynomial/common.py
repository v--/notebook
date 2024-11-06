from ...rings.arithmetic import IRing, ISemiring
from .base import BasePolynomial, PolynomialSubtractionMixin


class ISemiringPolynomial[N: ISemiring](BasePolynomial[N]):
    pass


class IRingPolynomial[N: IRing](PolynomialSubtractionMixin[N], ISemiringPolynomial[N]):
    pass
