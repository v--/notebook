from typing import overload

from ..graph import DirectedEdge
from .base import BaseGraphWalk, GraphWalkSegment


class DirectedWalk[VertT](BaseGraphWalk[VertT, DirectedEdge[VertT]]):
    @classmethod
    def from_vertex_list(cls, origin: VertT, *rest: VertT) -> DirectedWalk[VertT]:
        walk = cls(origin)

        for vertex in rest:
            walk.append(vertex)

        return walk

    def is_appendable(self, segment: GraphWalkSegment[VertT, DirectedEdge[VertT]]) -> bool:
        return self.tail == segment.edge.src

    @overload
    def append(self, vertex: VertT) -> None: ...
    @overload
    def append(self, segment: GraphWalkSegment[VertT, DirectedEdge[VertT]]) -> None: ...
    def append(self, *args, **kwargs) -> None:
        segment: GraphWalkSegment[VertT, DirectedEdge[VertT]] | None = kwargs.get('segment', None)

        if segment is None and len(args) > 0 and isinstance(args[0], GraphWalkSegment):
            segment = args[0]

        if segment is None:
            vertex: VertT = args[0]
            segment = GraphWalkSegment(DirectedEdge(self.tail, vertex), vertex)

        super().append(segment)
