from typing import Protocol


# Based on https://github.com/python/typing/issues/59#issuecomment-353878355
class IComparable(Protocol):
    def __eq__(self, other: object) -> bool:
        ...

    def __lt__[C](self: C, other: C) -> bool:
        ...

    def __gt__[C](self: C, other: C) -> bool:
        ...

    def __le__[C](self: C, other: C) -> bool:
        ...

    def __ge__[C](self: C, other: C) -> bool:
        ...
