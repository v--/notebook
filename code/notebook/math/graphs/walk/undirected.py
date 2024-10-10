import itertools
from collections.abc import Collection, Iterable, Sequence
from typing import override

from ..exceptions import GraphWalkError
from .base import GraphWalkType, get_tail


class UndirectedWalk[VertT, EdgeT: Collection](GraphWalkType[VertT, EdgeT]):
    origin: VertT
    arcs: Sequence[EdgeT]

    @classmethod
    def path(cls, origin: VertT, *rest: VertT) -> 'UndirectedWalk[VertT, frozenset[VertT]]':
        return UndirectedWalk(origin, [frozenset(pair) for pair in itertools.pairwise([origin, *rest])])

    def __init__(self, origin: VertT, arcs: Sequence[EdgeT]) -> None:
        current_tail = origin

        for edge in arcs:
            if current_tail not in edge:
                raise GraphWalkError(f'Invalid arc {edge} after {current_tail} in walk')

            current_tail = next(
                (v for v in edge if v != current_tail),
                current_tail
            )

        self.origin = origin
        self.arcs = arcs

    def __len__(self) -> int:
        return len(self.arcs)

    @override
    def iter_vertices(self) -> Iterable[VertT]:
        yield self.origin
        current_tail = self.origin

        for v1, v2 in self.arcs:
            current_tail = v2 if v1 == current_tail else v1
            yield current_tail

    def __str__(self) -> str:
        return ' → '.join(str(v) for v in self.iter_vertices())

    def __add__(self, other: object) -> 'UndirectedWalk[VertT, EdgeT]':
        if not isinstance(other, UndirectedWalk):
            return NotImplemented

        if get_tail(self) != other.origin:
            return NotImplemented

        return UndirectedWalk(
            self.origin,
            [*self.arcs, *other.arcs]
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UndirectedWalk):
            return NotImplemented

        return self.origin == other.origin and self.arcs == other.arcs
