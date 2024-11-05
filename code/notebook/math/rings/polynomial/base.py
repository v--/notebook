import contextlib
import functools
import itertools
from collections.abc import Callable, Iterable, Mapping, MutableMapping
from typing import Any, Self, override

from ....support.adt.arithmetic import IRing, ISemiring
from ....support.iteration import list_accumulator, string_accumulator
from .monomial import Monomial


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

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        result = super().__call__(*args, **kwargs)
        result.clone_zero = functools.partial(cls.__call__, *args, **kwargs)
        result.scalar_zero = cls.semiring(0)
        result.scalar_one = cls.semiring(1)
        return result


class BasePolynomial[T: ISemiring](metaclass=PolynomialMeta):
    coefficients: MutableMapping[Monomial, T]
    clone_zero: Callable[[], Self]
    scalar_zero: T
    scalar_one: T

    @classmethod
    def from_mapping(cls, coefficients: Mapping[Monomial, T] = {}) -> Self:
        result = cls()

        for mon, c in coefficients.items():
            result[mon] = c

        return result

    @classmethod
    def from_monomial(cls, monomial: Monomial) -> Self:
        result = cls()
        result[monomial] = result.scalar_one
        return result

    @classmethod
    @list_accumulator
    def from_monomials(cls, *monomials: Monomial) -> Iterable[Self]:
        for monomial in monomials:
            yield cls.from_monomial(monomial)

    def __init__(self) -> None:
        self.coefficients = {}

    @property
    def total_degree(self) -> int | None:
        return max((mon.total_degree for mon in self.coefficients.keys()), default=None)

    def __getitem__(self, key: Monomial) -> T:
        return self.coefficients.get(key, self.scalar_zero)

    def __setitem__(self, key: Monomial, value: T) -> None:
        if value == self.scalar_zero:
            with contextlib.suppress(KeyError):
                del self.coefficients[key]
        else:
            self.coefficients[key] = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BasePolynomial):
            return NotImplemented

        return self.coefficients == other.coefficients

    def __add__(self, other: Self) -> Self:
        result = self.clone_zero()

        for mon, c in self.coefficients.items():
            result[mon] = c

        for mon, c in other.coefficients.items():
            result[mon] += c

        return result

    def __mul__(self, other: Self) -> Self:
        result = self.clone_zero()

        for a, b in itertools.product(self.coefficients.keys(), other.coefficients.keys()):
            result[a * b] += self[a] * other[b]

        return result

    def __rmul__(self, other: T) -> Self:
        result = self.clone_zero()

        for mon, c in self.coefficients.items():
            result[mon] = c * other

        return result

    def __pow__(self, n: int) -> Self:
        result = self.clone_zero()

        for mon, c in self.coefficients.items():
            result[mon ** n] = c ** n

        for mon, c in self.coefficients.items():
            result[mon ** n] = c ** n

        return result

    @string_accumulator()
    def stringify_term_with_prefix(self, monomial: Monomial, coefficient: T, *, is_first: bool) -> Iterable[str]:
        if coefficient == 0:
            return

        if not is_first:
            yield ' + '

        if monomial.total_degree == 0 or coefficient != self.scalar_one:
            yield str(coefficient)

        if monomial.total_degree > 0:
            yield str(monomial)

    @string_accumulator()
    def __str__(self) -> Iterable[str]:
        it = iter(self.coefficients.items())

        try:
            monomial, coefficient = next(it)
        except StopIteration:
            yield str(self.scalar_zero)
            return  # noqa: PLE0307
        else:
            yield self.stringify_term_with_prefix(monomial, coefficient, is_first=True)

        for monomial, coefficient in it:
            yield self.stringify_term_with_prefix(monomial, coefficient, is_first=False)

    def __repr__(self) -> str:
        return str(self)


class PolynomialSubtractionMixin[T: IRing](BasePolynomial[T]):
    @override
    @string_accumulator()
    def stringify_term_with_prefix(self, monomial: Monomial, coefficient: T, *, is_first: bool) -> Iterable[str]:
        if coefficient == 0:
            return

        if is_first:
            if monomial.total_degree == 0:
                yield str(coefficient)
            elif coefficient == self.scalar_one:
                yield str(monomial)
            elif -coefficient == self.scalar_one:
                yield '-'
                yield str(monomial)
            else:
                yield str(coefficient)
                yield str(monomial)

            return

        using_negation = len(str(-coefficient)) < len(str(coefficient))

        if using_negation:
            yield ' - '

            if monomial.total_degree == 0 or -coefficient != self.scalar_one:
                yield str(-coefficient)
        else:
            yield ' + '

            if monomial.total_degree == 0 or coefficient != self.scalar_one:
                yield str(coefficient)

        if monomial.total_degree > 0:
            yield str(monomial)

    def __neg__(self: Self) -> Self:
        result = self.clone_zero()

        for mon, c in self.coefficients.items():
            try:
                result[mon] = -c
            except TypeError:
                return NotImplemented

        return result

    def __sub__(self, other: Self) -> Self:
        return self + (-other)
