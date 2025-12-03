import functools
import itertools
from collections.abc import Collection, Iterable
from typing import Self

from ...exceptions import UnreachableException
from ...support.unicode import itoa_subscripts
from ..strings import StringContainer


@functools.total_ordering
class BaseIdentifier(StringContainer):
    index: int | None

    def __init__(self, value: str, index: int | None = None) -> None:
        super().__init__(value)
        self.index = index

    def __str__(self) -> str:
        if self.index is None:
            return self.value

        return self.value + itoa_subscripts(self.index)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.value!r}, {self.index})'

    def __le__(self, other: Self) -> bool:
        self_index = self.index or 0
        other_index = other.index or 0
        return self.value <= other.value and self_index <= other_index

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseIdentifier):
            return False

        return self.value == other.value and self.index == other.index

    def __hash__(self) -> int:
        return hash((self.value, self.index))

    def increment(self) -> Self:
        return type(self)(
            self.value,
            0 if self.index is None else self.index + 1
        )


class LatinIdentifier(BaseIdentifier):
    pass


def iter_latin_identifiers() -> Iterable[LatinIdentifier]:
    for j in range(ord('a'), ord('z') + 1):
        yield LatinIdentifier(chr(j), index=None)

    for i in itertools.count(start=0):
        for j in range(ord('a'), ord('z') + 1):
            yield LatinIdentifier(chr(j), index=i)


def new_latin_identifier(blacklist: Collection[LatinIdentifier]) -> LatinIdentifier:
    for identifier in iter_latin_identifiers():
        if identifier not in blacklist:
            return identifier

    raise UnreachableException


class GreekIdentifier(BaseIdentifier):
    pass
