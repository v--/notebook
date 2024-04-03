import functools
import operator
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar, overload


T = TypeVar('T')


@dataclass
class Cycle(Generic[T]):
    payload: Sequence[T]

    def __str__(self) -> str:
        if len(self.payload) == 0:
            return 'id'

        return '(' + ' '.join(map(str, self.payload)) + ')'

    def __hash__(self) -> int:
        return functools.reduce(
            operator.xor,
            (hash(i) ^ hash(value) for i, value in enumerate(self.payload)),
            0
        )

    def __len__(self) -> int:
        return len(self.payload)

    def __iter__(self) -> Iterator[T]:
        return iter(self.payload)

    @overload
    def __getitem__(self, key: int) -> T:
        ...

    @overload
    def __getitem__(self, key: slice) -> Sequence[T]:
        ...

    def __getitem__(self, key: int | slice) -> T | Sequence[T]:
        return self.payload[key]

    def iter_decomposed(self) -> 'Iterable[Cycle]':
        if len(self.payload) < 2:
            yield Cycle([])
            return

        first = self.payload[0]

        for value in self.payload[1:]:
            yield Cycle([first, value])
