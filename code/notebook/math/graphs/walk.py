import itertools
from collections.abc import Iterable
from typing import Protocol, cast, override

from .exceptions import GraphError
from .generalized import GeneralizedArcT, VertT


class GraphWalkError(GraphError):
    pass


class GraphWalk(Protocol[VertT, GeneralizedArcT]):
    origin: VertT
    arcs: list[GeneralizedArcT]

    def __len__(self) -> int:
        ...

    def iter_vertices(self) -> Iterable[VertT]:
        ...

    def __add__(self, other: 'GraphWalk[VertT, GeneralizedArcT]') -> 'GraphWalk[VertT, GeneralizedArcT]':
        ...


def get_tail(walk: GraphWalk[VertT, GeneralizedArcT]) -> VertT:
    *_, last = walk.iter_vertices()
    return last


class DirectedWalk(GraphWalk[VertT, GeneralizedArcT]):
    origin: VertT
    arcs: list[GeneralizedArcT]

    @classmethod
    def simple(cls, origin: VertT, *rest: VertT) -> 'DirectedWalk[VertT, tuple[VertT, VertT]]':
        return DirectedWalk(origin, list(itertools.pairwise([origin, *rest])))

    def __init__(self, origin: VertT, arcs: list[GeneralizedArcT]) -> None:
        current_tail = origin

        for arc in arcs:
            src, dest = arc

            if src != current_tail:
                raise GraphWalkError(f'Invalid arc {arc} after {current_tail}')

            current_tail = cast(VertT, dest)

        self.origin = origin
        self.arcs = arcs

    def __len__(self) -> int:
        return len(self.arcs)

    @override
    def iter_vertices(self) -> Iterable[VertT]:
        yield self.origin

        for _, dest in self.arcs:
            yield cast(VertT, dest)

    def __str__(self) -> str:
        return ' → '.join(str(v) for v in self.iter_vertices())

    def __add__(self, other: object) -> 'DirectedWalk[VertT, GeneralizedArcT]':
        if not isinstance(other, DirectedWalk):
            return NotImplemented

        if get_tail(self) != other.origin:
            return NotImplemented

        return DirectedWalk(
            self.origin,
            self.arcs + other.arcs
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DirectedWalk):
            return NotImplemented

        return self.origin == other.origin and self.arcs == other.arcs


class UndirectedWalk(GraphWalk[VertT, GeneralizedArcT]):
    origin: VertT
    arcs: list[GeneralizedArcT]

    @classmethod
    def simple(cls, origin: VertT, *rest: VertT) -> 'UndirectedWalk[VertT, frozenset[VertT]]':
        return UndirectedWalk(origin, [frozenset(pair) for pair in itertools.pairwise([origin, *rest])])

    def __init__(self, origin: VertT, arcs: list[GeneralizedArcT]) -> None:
        current_tail = origin

        for edge in arcs:
            if current_tail not in edge:
                raise GraphWalkError(f'Invalid arc {edge} after {current_tail} in walk')

            current_tail = next(
                (cast(VertT, v) for v in edge if v != current_tail),
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
            current_tail = cast(VertT, v2 if v1 == current_tail else v1)
            yield current_tail

    def __str__(self) -> str:
        return ' → '.join(str(v) for v in self.iter_vertices())

    def __add__(self, other: object) -> 'UndirectedWalk[VertT, GeneralizedArcT]':
        if not isinstance(other, UndirectedWalk):
            return NotImplemented

        if get_tail(self) != other.origin:
            return NotImplemented

        return UndirectedWalk(
            self.origin,
            self.arcs + other.arcs
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DirectedWalk):
            return NotImplemented

        return self.origin == other.origin and self.arcs == other.arcs