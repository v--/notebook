import itertools
from collections.abc import Collection, Iterable, Sequence
from typing import override

from ..exceptions import GraphWalkError
from .base import GraphWalkType, get_tail


class DirectedWalk[VertT, EdgeT: Collection](GraphWalkType[VertT, EdgeT]):
    origin: VertT
    arcs: Sequence[EdgeT]

    @classmethod
    def path(cls, origin: VertT, *rest: VertT) -> 'DirectedWalk[VertT, tuple[VertT, VertT]]':
        return DirectedWalk(origin, list(itertools.pairwise([origin, *rest])))

    def __init__(self, origin: VertT, arcs: Sequence[EdgeT]) -> None:
        current_tail = origin

        for arc in arcs:
            src, dest = arc

            if src != current_tail:
                raise GraphWalkError(f'Invalid arc {arc} after {current_tail}')

            current_tail = dest

        self.origin = origin
        self.arcs = arcs

    def __len__(self) -> int:
        return len(self.arcs)

    @override
    def iter_vertices(self) -> Iterable[VertT]:
        yield self.origin

        for _, dest in self.arcs:
            yield dest

    def __str__(self) -> str:
        return ' → '.join(str(v) for v in self.iter_vertices())

    def __add__(self, other: object) -> 'DirectedWalk[VertT, EdgeT]':
        if not isinstance(other, DirectedWalk):
            return NotImplemented

        if get_tail(self) != other.origin:
            return NotImplemented

        return DirectedWalk(
            self.origin,
            [*self.arcs, *other.arcs]
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DirectedWalk):
            return NotImplemented

        return self.origin == other.origin and self.arcs == other.arcs
