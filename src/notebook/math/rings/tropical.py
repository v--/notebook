import operator
from typing import TYPE_CHECKING, Any, Self

from .exceptions import RingMetaError


if TYPE_CHECKING:
    from collections.abc import Callable


class TropicalMeta(type):
    sum: Callable[[float, float], float]
    zero: float

    def __new__[T: TropicalMeta](
        meta: type[T],
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        sum: Callable[[float, float], float] = operator.add,  # noqa: A002
        zero: float = 0,
    ) -> T:
        attrs['sum'] = sum
        attrs['zero'] = zero
        return type.__new__(meta, name, bases, attrs)

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        result = super().__call__(*args, **kwargs)
        result.new = cls
        return result


class BaseTropicalSemiring(metaclass=TropicalMeta):
    new: Callable[[float], Self]
    value: float

    def __init__(self, n: float) -> None:
        """Integers are lifted via the characteristic mapping, while floats are preserved literally."""
        if isinstance(n, int):
            if n < 0:
                raise RingMetaError(f'Expected a nonnegative integer, but got {n}')

            self.value = type(self).zero if n == 0 else 0.0
        else:
            self.value = n

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseTropicalSemiring):
            return NotImplemented

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __add__(self, other: Self) -> Self:
        return self.new(type(self).sum(self.value, other.value))

    def __mul__(self, other: Self) -> Self:
        return self.new(self.value + other.value)

    def __pow__(self, power: int) -> Self:
        result = self.new(1)

        for _ in range(power):
            result *= self

        return result

    def __float__(self) -> float:
        return self.value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return type(self).__name__ + '(' + str(self.value) + ')'


class MinPlusFloat(BaseTropicalSemiring, sum=min, zero=float('inf')):
    pass


class MaxPlusFloat(BaseTropicalSemiring, sum=max, zero=float('-inf')):
    pass
