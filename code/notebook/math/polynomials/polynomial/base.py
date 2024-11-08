import contextlib
import itertools
from collections.abc import Iterable, MutableMapping, Sequence
from typing import Any, Self, cast, override

from ....support.iteration import string_accumulator
from ...rings.types import IRing, ISemiring
from ..exceptions import PolynomialEvaluationError
from ..monomial import Monomial


class PolynomialMeta(type):
    semiring: type[ISemiring]

    def __new__[T: PolynomialMeta](
        meta: type[T],  # noqa: N804
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        semiring: type[ISemiring] = ISemiring,
    ) -> T:  # noqa: PYI019
        attrs['semiring'] = semiring
        return type.__new__(meta, name, bases, attrs)


class BasePolynomial[N: ISemiring](metaclass=PolynomialMeta):
    _coefficients: MutableMapping[Monomial, N]

    @classmethod
    def lift_to_scalar(cls, value: int) -> N:
        return cast(N, cls.semiring(value))

    @classmethod
    def new_zero(cls) -> Self:
        return cls()

    def __init__(self) -> None:
        self._coefficients = {}

    @property
    def total_degree(self) -> int | None:
        return max((mon.total_degree for mon in self._coefficients.keys()), default=None)

    @property
    def is_zero(self) -> bool:
        return len(self._coefficients) == 0

    def get_monomials(self) -> Sequence[Monomial]:
        return list(self._coefficients.keys())

    def __getitem__(self, key: Monomial) -> N:
        return self._coefficients.get(key, self.lift_to_scalar(0))

    def __setitem__(self, key: Monomial, value: N) -> None:
        if value == self.lift_to_scalar(0):
            with contextlib.suppress(KeyError):
                del self._coefficients[key]
        else:
            self._coefficients[key] = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BasePolynomial):
            return NotImplemented

        return self._coefficients == other._coefficients

    def __add__(self, other: Self) -> Self:
        pol = self.new_zero()

        for mon, c in self._coefficients.items():
            pol[mon] = c

        for mon, c in other._coefficients.items():
            pol[mon] += c

        return pol

    def __mul__(self, other: Self) -> Self:
        pol = self.new_zero()

        for a, b in itertools.product(self._coefficients.keys(), other._coefficients.keys()):
            pol[a * b] += self[a] * other[b]

        return pol

    def __rmul__(self, other: N) -> Self:
        pol = self.new_zero()

        for mon, c in self._coefficients.items():
            pol[mon] = c * other

        return pol

    def __pow__(self, power: int) -> Self:
        pol = self.new_zero()

        for mon, c in self._coefficients.items():
            pol[mon ** power] = c ** power

        for mon, c in self._coefficients.items():
            pol[mon ** power] = c ** power

        return pol

    @string_accumulator()
    def stringify_term_with_prefix(self, monomial: Monomial, coefficient: N, *, is_first: bool) -> Iterable[str]:
        if coefficient == 0:
            return

        if not is_first:
            yield ' + '

        if monomial.total_degree == 0 or coefficient != self.lift_to_scalar(1):
            yield str(coefficient)

        if monomial.total_degree > 0:
            yield str(monomial)

    @string_accumulator()
    def __str__(self) -> Iterable[str]:
        it = iter(self._coefficients.items())

        try:
            monomial, coefficient = next(it)
        except StopIteration:
            yield str(self.lift_to_scalar(0))
            return  # noqa: PLE0307
        else:
            yield self.stringify_term_with_prefix(monomial, coefficient, is_first=True)

        for monomial, coefficient in it:
            yield self.stringify_term_with_prefix(monomial, coefficient, is_first=False)

    def __repr__(self) -> str:
        return str(self)

    def __call__(self, **kwargs: N) -> N:
        result = self.lift_to_scalar(0)

        for mon, c in self._coefficients.items():
            term = c

            for indeterminate in mon.get_indeterminates():
                if indeterminate not in kwargs:
                    raise PolynomialEvaluationError(f'No value provided for indeterminate {indeterminate!r}')

                term *= kwargs[indeterminate] ** mon[indeterminate]

            result += term

        return result


class PolynomialSubtractionMixin[N: IRing](BasePolynomial[N]):
    @override
    @string_accumulator()
    def stringify_term_with_prefix(self, monomial: Monomial, coefficient: N, *, is_first: bool) -> Iterable[str]:
        if coefficient == 0:
            return

        if is_first:
            if monomial.total_degree == 0:
                yield str(coefficient)
            elif coefficient == self.lift_to_scalar(1):
                yield str(monomial)
            elif -coefficient == self.lift_to_scalar(1):
                yield '-'
                yield str(monomial)
            else:
                yield str(coefficient)
                yield str(monomial)

            return

        using_negation = len(str(-coefficient)) < len(str(coefficient))

        if using_negation:
            yield ' - '

            if monomial.total_degree == 0 or -coefficient != self.lift_to_scalar(1):
                yield str(-coefficient)
        else:
            yield ' + '

            if monomial.total_degree == 0 or coefficient != self.lift_to_scalar(1):
                yield str(coefficient)

        if monomial.total_degree > 0:
            yield str(monomial)

    def __neg__(self: Self) -> Self:
        pol = self.new_zero()

        for mon, c in self._coefficients.items():
            pol[mon] = -c

        return pol

    def __sub__(self, other: Self) -> Self:
        return self + (-other)
