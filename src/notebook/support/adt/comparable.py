from typing import Protocol, Self


# Based on https://github.com/python/typing/issues/59#issuecomment-353878355
class IComparable(Protocol):
    def __eq__(self, other: object) -> bool:
        ...

    def __lt__(self, other: Self) -> bool:
        ...

    def __gt__(self, other: Self) -> bool:
        ...

    def __le__(self, other: Self) -> bool:
        ...

    def __ge__(self, other: Self) -> bool:
        ...
