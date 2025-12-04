import contextlib
import itertools
from collections.abc import Iterable, MutableMapping, Sequence
from typing import Any, Self, cast, override

from ....parsing import LatinIdentifier, is_latin_identifier
from ....support.iteration import string_accumulator
from ....support.unicode import Capitalization
from ...rings.types import IRing, ISemiring
from ..exceptions import IndeterminateError, PolynomialError, PolynomialEvaluationError
from ..monomial import Monomial, const
from .degree import UNDEFINED_POLYNOMIAL_DEGREE, PolynomialDegree


class PolynomialMeta(type):
    semiring: type[ISemiring]

    def __new__[T: PolynomialMeta](
        meta: type[T],
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        semiring: type[ISemiring] = ISemiring,
    ) -> T:
        attrs['semiring'] = semiring
        return type.__new__(meta, name, bases, attrs)


class BasePolynomial[N: ISemiring](metaclass=PolynomialMeta):
    _coefficients: MutableMapping[Monomial, N]

    @classmethod
    def lift_to_scalar(cls, value: int) -> N:
        return cast('N', cls.semiring(value))

    @classmethod
    def new_zero(cls) -> Self:
        return cls()

    def __init__(self) -> None:
        self._coefficients = {}

    @property
    def total_degree(self) -> PolynomialDegree:
        return PolynomialDegree(
            max((mon.degree for mon in self._coefficients.keys()), default=None)
        )

    @property
    def is_zero(self) -> bool:
        return len(self._coefficients) == 0

    def get_indeterminates(self) -> Sequence[LatinIdentifier]:
        return sorted({indet for mon in self._coefficients for indet in mon.get_indeterminates()})

    def infer_inteterminate(self) -> LatinIdentifier:
        indeterminates = self.get_indeterminates()

        if len(indeterminates) == 0:
            raise PolynomialError('Cannot infer an indeterminate of a zero polynomial')

        if len(indeterminates) > 1:
            raise PolynomialError('Cannot infer an indeterminate of a multivariate polynomial')

        return indeterminates[0]

    def get_monomials(self) -> Sequence[Monomial]:
        return sorted(
            self._coefficients.keys(),
            key=lambda mon: [-mon.degree, mon.get_indeterminates()],
        )

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
        match power:
            case 1:
                return self

            case 0:
                pol = self.new_zero()
                pol[const] = self.lift_to_scalar(1)
                return pol

            case _ if power > 0:
                return self * self ** (power - 1)

        raise PolynomialError('Cannot raise a polynomial to a negative power')

    @string_accumulator()
    def stringify_term_with_prefix(self, monomial: Monomial, coefficient: N, *, is_first: bool) -> Iterable[str]:
        if coefficient == 0:
            return

        if not is_first:
            yield ' + '

        if monomial.degree == 0 or coefficient != self.lift_to_scalar(1):
            yield str(coefficient)

        if monomial.degree > 0:
            yield str(monomial)

    @string_accumulator()
    def __str__(self) -> Iterable[str]:
        it = iter(self.get_monomials())

        try:
            mon = next(it)
        except StopIteration:
            yield str(self.lift_to_scalar(0))
            return  # noqa: PLE0307
        else:
            yield self.stringify_term_with_prefix(mon, self[mon], is_first=True)

        for mon in it:
            yield self.stringify_term_with_prefix(mon, self[mon], is_first=False)

    def __repr__(self) -> str:
        return str(self)

    def __call__(self, **kwargs: N) -> N:
        for key in kwargs.keys():
            if not is_latin_identifier(key, capitalization=Capitalization.LOWER):
                raise IndeterminateError(f'The parameter name {key} is not a valid indeterminate name.') from None

        result = self.lift_to_scalar(0)

        for mon, c in self._coefficients.items():
            term = c

            for indeterminate in mon.get_indeterminates():
                if str(indeterminate) not in kwargs:
                    raise PolynomialEvaluationError(f'No value provided for the indeterminate {str(indeterminate)!r}')

                term *= kwargs[str(indeterminate)] ** mon[indeterminate]

            result += term

        return result

    def get_max_power(self, indet: LatinIdentifier | None = None) -> int:
        max_power = 0

        if self.is_zero:
            return max_power

        if indet is None:
            indet = self.infer_inteterminate()

        for mon in self.get_monomials():
            if indet in mon.get_indeterminates() and mon[indet] > max_power:
                max_power = mon[indet]

        return max_power

    def get_degree(self, indet: LatinIdentifier | None = None) -> PolynomialDegree:
        if self.is_zero:
            return UNDEFINED_POLYNOMIAL_DEGREE

        return PolynomialDegree(self.get_max_power(indet))

    def leading_coefficient(self, indet: LatinIdentifier | None = None) -> Self:
        result = self.new_zero()

        if self.is_zero:
            return result

        if indet is None:
            indet = self.infer_inteterminate()

        n = self.get_max_power(indet)

        for mon in self.get_monomials():
            if mon[indet] == n:
                new_mon = Monomial({ind: mon[ind] for ind in mon if ind != indet})
                result[new_mon] = self[mon]

        return result


class PolynomialSubtractionMixin[N: IRing](BasePolynomial[N]):
    @override
    @string_accumulator()
    def stringify_term_with_prefix(self, monomial: Monomial, coefficient: N, *, is_first: bool) -> Iterable[str]:
        if coefficient == 0:
            return

        if is_first:
            if monomial.degree == 0:
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

            if monomial.degree == 0 or -coefficient != self.lift_to_scalar(1):
                yield str(-coefficient)
        else:
            yield ' + '

            if monomial.degree == 0 or coefficient != self.lift_to_scalar(1):
                yield str(coefficient)

        if monomial.degree > 0:
            yield str(monomial)

    def __neg__(self: Self) -> Self:
        pol = self.new_zero()

        for mon, c in self._coefficients.items():
            pol[mon] = -c

        return pol

    def __sub__(self, other: Self) -> Self:
        return self + (-other)
