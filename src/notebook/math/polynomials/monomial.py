import functools
from collections.abc import Hashable, Iterable, Iterator, Mapping, Sequence
from typing import Self

from ...parsing import LatinIdentifier
from ...parsing import common_identifiers as ci
from ...support.iteration import string_accumulator
from ...support.unicode import to_superscript


@functools.total_ordering
class Monomial(Mapping[LatinIdentifier, int], Hashable):
    _payload: Mapping[LatinIdentifier, int]

    @classmethod
    def from_indeterminate(cls, indeterminate: LatinIdentifier) -> Self:
        return cls({indeterminate: 1})

    def __init__(self, payload: Mapping[LatinIdentifier, int]) -> None:
        self._payload = {ind: pwr for ind, pwr in payload.items() if pwr != 0}

    @property
    def degree(self) -> int:
        return sum(self._payload.values())

    def get_indeterminates(self) -> Sequence[LatinIdentifier]:
        return sorted(self._payload.keys())

    def __len__(self) -> int:
        return len(self._payload)

    def __iter__(self) -> Iterator[LatinIdentifier]:
        return iter(sorted(self._payload.keys()))

    def __getitem__(self, indeterminate: LatinIdentifier) -> int:
        return self._payload.get(indeterminate, 0)

    def __mul__(self, other: Monomial) -> Monomial:
        return Monomial({
            ind: self[ind] + other[ind]
            for ind in {*self.get_indeterminates(), *other.get_indeterminates()}
        })

    def __pow__(self, power: int) -> Monomial:
        return Monomial({
            indeterminate: p * power
            for indeterminate, p in self._payload.items()
        })

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Monomial):
            return NotImplemented

        return self._payload == other._payload

    def __le__(self, other: Monomial) -> bool:
        if self.degree > other.degree:
            return True

        for ind in sorted({*self.get_indeterminates(), *other.get_indeterminates()}):
            if self._payload.get(ind, 0) < other._payload.get(ind, 0):
                return True

        return False

    @string_accumulator()
    def __str__(self) -> Iterable[str]:
        if len(self._payload) == 0:
            yield '1'
            return  # noqa: PLE0307

        for ind in iter(self):
            yield str(ind)
            power = self[ind]

            if power > 1:
                yield to_superscript(str(power))

    def __hash__(self) -> int:
        return hash(tuple(dict(self).items()))


x = Monomial({ ci.x: 1 })
y = Monomial({ ci.y: 1 })
z = Monomial({ ci.z: 1 })
const = Monomial({})
