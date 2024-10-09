from typing import NamedTuple

from .binary_edge import BinaryEdgeView


class DirectedEdge[VertT](NamedTuple):
    src: VertT
    dest: VertT


class DirectedEdgeView[VertT, VertLabelT, EdgeLabelT](BinaryEdgeView[VertT, DirectedEdge[VertT], VertLabelT, EdgeLabelT], edge_class=DirectedEdge):
    pass
