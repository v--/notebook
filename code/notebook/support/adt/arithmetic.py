from typing import Literal, Protocol, Self, runtime_checkable


@runtime_checkable
class ISemiring(Protocol):
    def __init__(self, value: Literal[0, 1]) -> None:
        ...

    def __add__(self, other: Self) -> Self:
        ...

    def __mul__(self, other: Self) -> Self:
        ...

    def __pow__(self, power: int) -> Self:
        ...


@runtime_checkable
class IRing(ISemiring, Protocol):
    def __sub__(self, other: Self) -> Self:
        ...

    def __neg__(self) -> Self:
        ...


@runtime_checkable
class IField(IRing, Protocol):
    def __div__(self, other: Self) -> Self:
        ...
