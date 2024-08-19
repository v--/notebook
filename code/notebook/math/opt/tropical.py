from collections.abc import Callable
from typing import Any, Never, TypeVar

from ...exceptions import NotebookCodeError


class TropicalArithmeticError(NotebookCodeError):
    pass


class TropicalSubtractionError(TropicalArithmeticError):
    pass


class TropicalDivisionError(TropicalArithmeticError):
    pass


T = TypeVar('T', bound='TropicalMeta')


class TropicalMeta(type):
    @staticmethod
    def sub(a: T, b: T) -> Never:  # noqa: ARG004
        raise TropicalSubtractionError('Cannot subtract in tropical semirings')

    @staticmethod
    def div(a: T, b: T) -> Never:  # noqa: ARG004
        raise TropicalDivisionError('Cannot subtract in tropical semirings')

    def __new__(meta: 'type[TropicalMeta]', name: str, bases: tuple[type, ...], attrs: dict[str, Any], add: Callable[[T, T], T], mul: Callable[[T, T], T]) -> 'TropicalMeta':  # noqa: N804
        attrs['__radd__'] = attrs['__add__'] = lambda self, other: cls(add(self, other))
        attrs['__rmul__'] = attrs['__mul__'] = lambda self, other: cls(mul(self, other))
        attrs['__rsub__'] = attrs['__sub__'] = meta.sub
        attrs['__rtruediv__'] = attrs['__truediv__'] = meta.div
        attrs['__rfloordiv__'] = attrs['__floordiv__'] = meta.div
        cls: TropicalMeta = type.__new__(meta, name, bases, attrs)
        return cls


class MinPlusFloat(float, metaclass=TropicalMeta, add=min, mul=float.__add__):
    pass


class MaxPlusFloat(float, metaclass=TropicalMeta, add=max, mul=float.__add__):
    pass