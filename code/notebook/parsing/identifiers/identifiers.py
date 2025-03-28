import itertools
from collections.abc import Collection, Iterable
from typing import Self

from ...exceptions import UnreachableException
from ...support.unicode import itoa_subscripts
from ..strings import StringContainer


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
