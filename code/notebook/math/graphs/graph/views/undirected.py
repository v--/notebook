from typing import NamedTuple

from .binary_edge import BinaryEdgeView


class UndirectedEdge[VertT](NamedTuple):
    src: VertT
    dest: VertT

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UndirectedEdge):
            return NotImplemented

        return (self.src == other.src and self.dest == other.dest) or (self.src == other.dest and self.dest == other.src)


class UndirectedEdgeView[VertT, VertLabelT, EdgeLabelT](BinaryEdgeView[VertT, UndirectedEdge[VertT], VertLabelT, EdgeLabelT], edge_class=UndirectedEdge):
    pass
