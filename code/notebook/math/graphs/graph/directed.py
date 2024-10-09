from .base import BaseGraph
from .views.directed import DirectedEdge, DirectedEdgeView
from .views.vertex import VertexView


class DirectedGraph[VertT, VertLabelT, EdgeLabelT](BaseGraph[VertT, DirectedEdge[VertT], VertLabelT, EdgeLabelT], edge_view=DirectedEdgeView):
    vertices: VertexView[VertT, DirectedEdge[VertT], VertLabelT, EdgeLabelT]
    edges: DirectedEdgeView[VertT, VertLabelT, EdgeLabelT]
