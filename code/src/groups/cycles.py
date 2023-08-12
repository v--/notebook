from collections.abc import MutableMapping, Sequence
from dataclasses import dataclass
from typing import TypeVar, Generic
import functools
import operator


T = TypeVar('T')


@dataclass
class Cycle(Generic[T]):
    payload: Sequence[T]

    def __str__(self):
        if len(self.payload) == 0:
            return 'id'

        return '(' + ' '.join(map(str, self.payload)) + ')'

    def __hash__(self):
        return functools.reduce(
            operator.xor,
            (hash(i) ^ hash(value) for i, value in enumerate(self.payload)),
            0
        )

    def __len__(self):
        return len(self.payload)

    def __iter__(self):
        return iter(self.payload)

    def __getitem__(self, key: int | slice):
        return self.payload[key]

    def iter_decomposed(self):
        if len(self.payload) < 2:
            yield Cycle([])
            return

        first = self.payload[0]

        for value in self.payload[1:]:
            yield Cycle([first, value])
