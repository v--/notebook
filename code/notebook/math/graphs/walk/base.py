from collections.abc import Collection, Iterable, Sequence
from typing import Protocol


class GraphWalkType[VertT, EdgeT: Collection](Protocol):
    origin: VertT
    arcs: Sequence[EdgeT]

    def __len__(self) -> int:
        ...

    def iter_vertices(self) -> Iterable[VertT]:
        ...

    def __add__(self, other: 'GraphWalkType[VertT, EdgeT]') -> 'GraphWalkType[VertT, EdgeT]':
        ...


def get_tail[VertT, EdgeT: Collection](walk: GraphWalkType[VertT, EdgeT]) -> VertT:
    *_, last = walk.iter_vertices()
    return last
