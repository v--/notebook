from collections.abc import Callable
from typing import Any, Self

from ..arithmetic.divisibility import rem


class IntModuloMeta(type):
    modulus: int

    def __new__[T: IntModuloMeta](
        meta: type[T],  # noqa: N804
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        modulus: int = 2,
    ) -> T:  # noqa: PYI019
        assert modulus > 1
        attrs['modulus'] = modulus
        return type.__new__(meta, name, bases, attrs)

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        result = super().__call__(*args, **kwargs)
        result.modulus = cls.modulus
        result.new = cls
        return result


class BaseIntModulo(metaclass=IntModuloMeta):
    new: Callable[[int], Self]
    modulus: int
    value: int

    def __init__(self, n: int) -> None:
        self.value = rem(n, self.modulus)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseIntModulo):
            return NotImplemented

        return self.value == other.value

    def __add__(self, other: Self | int) -> Self:
        if isinstance(other, BaseIntModulo):
            return self.new(self.value + other.value)

        return self.new(self.value + other)

    def __neg__(self) -> Self:
        return self.new(self.modulus - self.value)

    def __sub__(self, other: Self | int) -> Self:
        return self + (-other)

    def __mul__(self, other: Self | int) -> Self:
        if isinstance(other, BaseIntModulo):
            return self.new(self.value * other.value)

        return self.new(self.value * other)

    def __pow__(self, power: int) -> Self:
        return self.new(self.value ** power)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return type(self).__name__ + '(' + str(self.value) + ')'


class Z2(BaseIntModulo, modulus=2):
    pass


class Z3(BaseIntModulo, modulus=3):
    pass
