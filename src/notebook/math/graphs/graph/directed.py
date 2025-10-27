from .base import BaseGraph
from .views.directed import DirectedEdge, DirectedEdgeView
from .views.vertex import VertexView


class DirectedGraph[VertT, VertLabelT, EdgeSymbolT](BaseGraph[VertT, DirectedEdge[VertT], VertLabelT, EdgeSymbolT], edge_view=DirectedEdgeView):
    vertices: VertexView[VertT, DirectedEdge[VertT], VertLabelT, EdgeSymbolT]
    edges: DirectedEdgeView[VertT, VertLabelT, EdgeSymbolT]
