import functools
from collections.abc import Hashable, Iterable, Iterator, Mapping, Sequence
from typing import Self

from ....support.iteration import string_accumulator
from ....support.unicode import to_superscript


@functools.total_ordering
class Monomial(Mapping[str, int], Hashable):
    payload: Mapping[str, int]

    @classmethod
    def from_indeterminate(cls, indeterminate: str) -> Self:
        return cls(**{indeterminate: 1})

    def __init__(self, **kwargs: int) -> None:
        self.payload = kwargs

    @property
    def total_degree(self) -> int:
        return sum(self.payload.values())

    def get_indeterminates(self) -> Sequence[str]:
        return list(self.payload.keys())

    def __len__(self) -> int:
        return len(self.payload)

    def __iter__(self) -> Iterator[str]:
        return iter(sorted(self.payload.keys()))

    def __getitem__(self, indeterminate: str) -> int:
        return self.payload.get(indeterminate, 0)

    def __mul__(self, other: 'Monomial') -> 'Monomial':
        return Monomial(**{
            indeterminate: self[indeterminate] + other[indeterminate]
            for indeterminate in {*self.get_indeterminates(), *other.get_indeterminates()}
        })

    def __pow__(self, power: int) -> 'Monomial':
        return Monomial(**{
            indeterminate: p * power
            for indeterminate, p in self.payload.items()
        })

    def __eq__(self, other: 'object') -> bool:
        if not isinstance(other, Monomial):
            return NotImplemented

        return self.payload == other.payload

    def __le__(self, other: 'Monomial') -> bool:
        if self.total_degree > other.total_degree:
            return True

        for indeterminate in sorted({*self.get_indeterminates(), *other.get_indeterminates()}):
            if self.payload.get(indeterminate, 0) < other.payload.get(indeterminate, 0):
                return True

        return False

    @string_accumulator()
    def __str__(self) -> Iterable[str]:
        if len(self.payload) == 0:
            yield '1'
            return  # noqa: PLE0307

        for indeterminate in iter(self):
            yield indeterminate
            power = self[indeterminate]

            if power > 1:
                yield to_superscript(str(power))

    def __hash__(self) -> int:
        return hash(str(self))


x = Monomial(x=1)
y = Monomial(y=1)
z = Monomial(z=1)
const = Monomial()
