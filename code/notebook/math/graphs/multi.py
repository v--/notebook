from collections.abc import Collection, Hashable
from typing import Generic, Iterator

from .generalized import ArcLabelT, GeneralizedDirectedGraph, GeneralizedUndirectedGraph, VertLabelT, VertT


class MultiArc(Generic[VertT], Collection[Hashable]):
    _counter: int = 0  # Static

    src: VertT
    dest: VertT
    _id: int

    def __new__(cls: 'type[MultiArc]', src: VertT, dest: VertT) -> 'MultiArc':  # noqa: ARG003
        cls._counter += 1
        return super().__new__(cls)

    def __init__(self, src: VertT, dest: VertT) -> None:
        self.src = src
        self.dest = dest
        self._id = self._counter

    def __contains__(self, other: object) -> bool:
        return self.src == other or self.dest == other

    def __iter__(self) -> Iterator[VertT]:
        yield self.src
        yield self.dest

    def __len__(self) -> int:
        return 2

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MultiArc):
            return NotImplemented

        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return self._id


class DirectedMultigraph(GeneralizedDirectedGraph[VertT, MultiArc[VertT], VertLabelT, ArcLabelT]):
    pass


class MultiEdge(MultiArc[VertT]):
    def __len__(self) -> int:
        if self.src == self.dest:
            return 1

        return 2


class UndirectedMultigraph(GeneralizedUndirectedGraph[VertT, MultiEdge[VertT], VertLabelT, ArcLabelT]):
    pass
