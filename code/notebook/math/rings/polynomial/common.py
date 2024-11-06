from ...rings.types import IField, IRing, ISemiring
from .base import BasePolynomial, PolynomialSubtractionMixin
from .constructor import PolynomialConstructorMixin


class ISemiringPolynomial[N: ISemiring](PolynomialConstructorMixin[N], BasePolynomial[N]):
    pass


class IRingPolynomial[N: IRing](PolynomialSubtractionMixin[N], ISemiringPolynomial[N]):
    pass


class IFieldPolynomial[N: IField](IRingPolynomial[N]):
    pass
