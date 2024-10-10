from typing import NamedTuple

from .binary_edge import BinaryEdgeView


class DirectedEdge[VertT](NamedTuple):
    src: VertT
    dest: VertT


class DirectedEdgeView[VertT, VertLabelT, EdgeSymbolT](BinaryEdgeView[VertT, DirectedEdge[VertT], VertLabelT, EdgeSymbolT], edge_class=DirectedEdge):
    pass
