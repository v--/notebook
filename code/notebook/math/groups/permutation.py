from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar

from ...support.adt.comparable import Comparable
from .cycle import Cycle


T = TypeVar('T', bound=Comparable)
PermutationT = TypeVar('PermutationT', bound='Permutation')


@dataclass
class Permutation(Generic[T]):
    domain: Sequence[T]
    _payload: Mapping[T, T]

    @classmethod
    def from_incomplete_mapping(cls: type[PermutationT], domain: Sequence[T], incomplete: Mapping[T, T]) -> PermutationT:
        complete = {}

        for key in list(incomplete):
            value = incomplete[key]

            if key == value:
                continue

            complete[key] = value

            if value not in incomplete:
                complete[value] = key

        return cls(domain, complete)

    @classmethod
    def from_cycle(cls, domain: Sequence[T], cycle: Cycle[T]) -> 'Permutation[T]':
        if len(cycle) == 0:
            return Permutation(domain, {})

        mapping = {cycle[-1]: cycle[0]}

        for src, dest in zip(cycle[:-1], cycle[1:]):
            mapping[src] = dest

        return Permutation(domain, mapping)

    @classmethod
    def identity(cls, domain: Sequence[T]) -> 'Permutation[T]':
        return Permutation(domain, {})

    def __getitem__(self, key: T) -> T:
        return self._payload.get(key, key)

    def get_mapping(self) -> dict[T, T]:
        return {key: self[key] for key in self.domain}

    @property
    def values(self) -> Sequence[T]:
        return sorted(self._payload)

    def __matmul__(self, other: 'Permutation[T]') -> 'Permutation[T]':
        if not isinstance(other, Permutation):
            return NotImplemented

        mapping = dict(self._payload)

        for key in other.values:
            if other[key] in self._payload:
                mapping[key] = self._payload[other[key]]
            else:
                mapping[key] = other[key]

        return Permutation(self.domain, mapping)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Permutation) or self.domain != other.domain:
            return NotImplemented

        return self.get_mapping() == other.get_mapping()

    def inverse(self) -> 'Permutation[T]':
        return Permutation(self.domain, {self[value]: value for value in self.values})

    def iter_decomposed(self) -> Iterable[Cycle[T]]:
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

