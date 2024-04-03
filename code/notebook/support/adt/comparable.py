import typing
from typing import Protocol


C = typing.TypeVar('C', bound='Comparable')


# Based on https://github.com/python/typing/issues/59#issuecomment-353878355
class Comparable(Protocol):
    def __eq__(self, other: object) -> bool:
        pass

    def __lt__(self: C, other: C) -> bool:
        pass

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other
