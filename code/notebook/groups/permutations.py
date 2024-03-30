from collections.abc import Iterable, Iterator, MutableMapping
from dataclasses import dataclass
from typing import Generic, TypeVar

from rich import box
from rich.table import Table

from ..support.rich import rich_to_text
from .cycles import Cycle


T = TypeVar('T')


@dataclass
class Permutation(Generic[T]):
    mapping: MutableMapping[T, T]

    @classmethod
    def from_incomplete_mapping(cls, incomplete: MutableMapping[T, T]):
        complete = {}

        for key in list(incomplete):
            value = incomplete[key]
            complete[key] = value

            if value not in incomplete:
                complete[value] = key

        return cls(complete)

    @classmethod
    def from_cycle(cls, cycle: Cycle[T]):
        if len(cycle) == 0:
            return Permutation({})

        mapping = {cycle[-1]: cycle[0]}

        for src, dest in zip(cycle[:-1], cycle[1:]):
            mapping[src] = dest

        return Permutation(mapping)

    @classmethod
    def identity(cls, values: Iterable[T]):
        return Permutation({value: value for value in values})

    def __getitem__(self, key: T):
        return self.mapping[key]

    @property
    def values(self):
        return sorted(self.mapping)

    def __str__(self):
        table = Table(box=box.SIMPLE)
        keys = self.values

        for key in keys:
            table.add_column(str(key))

        table.add_row(*(str(self[key]) for key in keys))
        return rich_to_text(table)

    def __matmul__(self, other: object):
        if not isinstance(other, Permutation):
            return NotImplemented

        mapping = dict(self.mapping)

        for key in other.values:
            if other[key] in self.mapping:
                mapping[key] = self.mapping[other[key]]
            else:
                mapping[key] = other[key]

        return Permutation(mapping)

    def inverse(self):
        return Permutation({self[value]: value for value in self.values})

    def iter_decomposed(self) -> Iterator[Cycle[T]]:
        consumed_values = set()

        for value in self.values:
            if value in consumed_values:
                continue

            consumed_values.add(value)
            cycle_payload = [value]
            current = value

            while self[current] not in cycle_payload:
                current = self[current]
                consumed_values.add(current)
                cycle_payload.append(current)

            yield Cycle(cycle_payload)

