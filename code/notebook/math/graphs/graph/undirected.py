from .base import BaseGraph
from .views.undirected import UndirectedEdge, UndirectedEdgeView
from .views.vertex import VertexView


class UndirectedGraph[VertT, VertLabelT, EdgeLabelT](BaseGraph[VertT, UndirectedEdge[VertT], VertLabelT, EdgeLabelT], edge_view=UndirectedEdgeView):
    vertices: VertexView[VertT, UndirectedEdge[VertT], VertLabelT, EdgeLabelT]
    edges: UndirectedEdgeView[VertT, VertLabelT, EdgeLabelT]
