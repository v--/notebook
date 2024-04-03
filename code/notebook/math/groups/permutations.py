from collections.abc import Iterable, Iterator, MutableMapping, Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar

from rich import box
from rich.table import Table

from ...support.adt.comparable import Comparable
from ...support.rich import rich_to_text
from .cycles import Cycle


T = TypeVar('T', bound=Comparable)
PermutationT = TypeVar('PermutationT', bound='Permutation')


@dataclass
class Permutation(Generic[T]):
    mapping: MutableMapping[T, T]

    @classmethod
    def from_incomplete_mapping(cls: type[PermutationT], incomplete: MutableMapping[T, T]) -> PermutationT:
        complete = {}

        for key in list(incomplete):
            value = incomplete[key]
            complete[key] = value

            if value not in incomplete:
                complete[value] = key

        return cls(complete)

    @classmethod
    def from_cycle(cls, cycle: Cycle[T]) -> 'Permutation[T]':
        if len(cycle) == 0:
            return Permutation({})

        mapping = {cycle[-1]: cycle[0]}

        for src, dest in zip(cycle[:-1], cycle[1:]):
            mapping[src] = dest

        return Permutation(mapping)

    @classmethod
    def identity(cls, values: Iterable[T]) -> 'Permutation[T]':
        return Permutation({value: value for value in values})

    def __getitem__(self, key: T) -> T:
        return self.mapping[key]

    @property
    def values(self) -> Sequence[T]:
        return sorted(self.mapping)

    def __str__(self) -> str:
        table = Table(box=box.SIMPLE)
        keys = self.values

        for key in keys:
            table.add_column(str(key))

        table.add_row(*(str(self[key]) for key in keys))
        return rich_to_text(table)

    def __matmul__(self, other: 'Permutation[T]') -> 'Permutation[T]':
        if not isinstance(other, Permutation):
            return NotImplemented

        mapping = dict(self.mapping)

        for key in other.values:
            if other[key] in self.mapping:
                mapping[key] = self.mapping[other[key]]
            else:
                mapping[key] = other[key]

        return Permutation(mapping)

    def inverse(self) -> 'Permutation[T]':
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

