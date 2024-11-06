from collections.abc import Iterable, Mapping
from typing import Self, cast

from ....support.iteration import list_accumulator
from ..arithmetic import ISemiring
from .base import BasePolynomial
from .monomial import Monomial, const


class PolynomialConstructorMixin[N: ISemiring](BasePolynomial[N]):
    @classmethod
    def lift(cls, value: N | int) -> Self:
        pol = cls()

        if isinstance(value, int):
            pol[const] = cast(N, cls.semiring(value))
        else:
            pol[const] = value

        return pol

    @classmethod
    def from_mapping(cls, coefficients: Mapping[Monomial, N] = {}) -> Self:
        pol = cls()

        for mon, c in coefficients.items():
            pol[mon] = c

        return pol

    @classmethod
    def from_monomial(cls, monomial: Monomial) -> Self:
        pol = cls()
        pol[monomial] = cast(N, cls.semiring(1))
        return pol

    @classmethod
    @list_accumulator
    def from_monomials(cls, *monomials: Monomial) -> Iterable[Self]:
        for monomial in monomials:
            yield cls.from_monomial(monomial)
