import itertools
from collections.abc import Iterable
from typing import Self, TypeVar

from ..support.unicode import itoa_subscripts
from .tokens import TokenMixin


class Identifier(TokenMixin):
    index: int | None

    @classmethod
    def build(cls: type[Self], value: str, index: int | None = None) -> Self:
        return cls(value, index)

    def __init__(self, value: str, index: int | None = None) -> None:
        super().__init__(value)
        self.index = index

    def __str__(self) -> str:
        if self.index is None:
            return self.value

        return self.value + itoa_subscripts(self.index)

    def increment(self) -> Self:
        return type(self).build(
            self.value,
            0 if self.index is None else self.index + 1
        )


IdentifierT = TypeVar('IdentifierT', bound=Identifier)


class LatinIdentifier(Identifier):
    pass


def iter_latin_identifiers() -> Iterable[LatinIdentifier]:
    for j in range(ord('a'), ord('z') + 1):
        yield LatinIdentifier(chr(j), index=None)

    for i in itertools.count(start=0):
        for j in range(ord('a'), ord('z') + 1):
            yield LatinIdentifier(chr(j), index=i)


def new_latin_identifier(context: frozenset[LatinIdentifier]) -> LatinIdentifier:
    for identifier in iter_latin_identifiers():
        if identifier not in context:
            return identifier

    raise AssertionError('This unreachable code is here to satisfy mypy and ruff')


class GreekIdentifier(Identifier):
    pass
