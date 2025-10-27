from typing import NamedTuple

from .binary_edge import BinaryEdgeView


class DirectedMultiedge[VertT](NamedTuple):
    src: VertT
    dest: VertT

    def __eq__(self, other: object) -> bool:
        return id(self) == id(other)


class DirectedMultiedgeView[VertT, VertLabelT, EdgeSymbolT](BinaryEdgeView[VertT, DirectedMultiedge[VertT], VertLabelT, EdgeSymbolT], edge_class=DirectedMultiedge):
    pass
