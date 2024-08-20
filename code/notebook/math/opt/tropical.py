from collections.abc import Callable
from typing import Any, Never

from ...exceptions import NotebookCodeError


class TropicalArithmeticError(NotebookCodeError):
    pass


class TropicalSubtractionError(TropicalArithmeticError):
    pass


class TropicalDivisionError(TropicalArithmeticError):
    pass


class TropicalMeta(type):
    @staticmethod
    def sub[T: TropicalMeta](a: T, b: T) -> Never:  # noqa: ARG004
        raise TropicalSubtractionError('Cannot subtract in tropical semirings')

    @staticmethod
    def div[T: TropicalMeta](a: T, b: T) -> Never:  # noqa: ARG004
        raise TropicalDivisionError('Cannot subtract in tropical semirings')

    def __new__[T: TropicalMeta](meta: type[T], name: str, bases: tuple[type, ...], attrs: dict[str, Any], add: Callable[[T, T], T], mul: Callable[[T, T], T]) -> T:  # noqa: N804, PYI019
        attrs['__radd__'] = attrs['__add__'] = lambda self, other: cls(add(self, other))
        attrs['__rmul__'] = attrs['__mul__'] = lambda self, other: cls(mul(self, other))
        attrs['__rsub__'] = attrs['__sub__'] = meta.sub
        attrs['__rtruediv__'] = attrs['__truediv__'] = meta.div
        attrs['__rfloordiv__'] = attrs['__floordiv__'] = meta.div
        cls: T = type.__new__(meta, name, bases, attrs)
        return cls


class MinPlusFloat(float, metaclass=TropicalMeta, add=min, mul=float.__add__):
    pass


class MaxPlusFloat(float, metaclass=TropicalMeta, add=max, mul=float.__add__):
    pass
