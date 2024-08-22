from collections.abc import Collection, Iterator

from .generalized import BaseVertType, GeneralizedDirectedGraph, GeneralizedUndirectedGraph


class MultiArc[VertT: BaseVertType](Collection[VertT]):
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


class DirectedMultigraph[VertT: BaseVertType, VertLabelT, ArcLabelT](GeneralizedDirectedGraph[VertT, MultiArc[VertT], VertLabelT, ArcLabelT]):
    pass


class MultiEdge[VertT](MultiArc[VertT]):
    def __len__(self) -> int:
        if self.src == self.dest:
            return 1

        return 2


class UndirectedMultigraph[VertT: BaseVertType, VertLabelT, ArcLabelT](GeneralizedUndirectedGraph[VertT, MultiEdge[VertT], VertLabelT, ArcLabelT]):
    pass
