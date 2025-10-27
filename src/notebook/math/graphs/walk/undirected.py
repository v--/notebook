from typing import overload

from ..graph import UndirectedEdge
from .base import BaseGraphWalk, GraphWalkSegment


class UndirectedWalk[VertT](BaseGraphWalk[VertT, UndirectedEdge[VertT]]):
    @classmethod
    def from_vertex_list(cls, origin: VertT, *rest: VertT) -> UndirectedWalk[VertT]:
        walk = cls(origin)

        for vertex in rest:
            walk.append(vertex)

        return walk

    @overload
    def append(self, vertex: VertT) -> None: ...
    @overload
    def append(self, segment: GraphWalkSegment[VertT, UndirectedEdge[VertT]]) -> None: ...
    def append(self, *args, **kwargs) -> None:
        segment: GraphWalkSegment[VertT, UndirectedEdge[VertT]] | None = kwargs.get('segment', None)

        if segment is None and len(args) > 0 and isinstance(args[0], GraphWalkSegment):
            segment = args[0]

        if segment is None:
            vertex: VertT = args[0]
            segment = GraphWalkSegment(UndirectedEdge(self.tail, vertex), vertex)

        super().append(segment)
