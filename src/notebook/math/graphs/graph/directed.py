from typing import TYPE_CHECKING

from .base import BaseGraph
from .views.directed import DirectedEdge, DirectedEdgeView


if TYPE_CHECKING:
    from .views.vertex import VertexView


class DirectedGraph[VertT, VertLabelT = None, EdgeLabelT = None](BaseGraph[VertT, DirectedEdge[VertT], VertLabelT, EdgeLabelT], edge_view=DirectedEdgeView):
    vertices: VertexView[VertT, DirectedEdge[VertT], VertLabelT, EdgeLabelT]
    edges: DirectedEdgeView[VertT, VertLabelT, EdgeLabelT]
