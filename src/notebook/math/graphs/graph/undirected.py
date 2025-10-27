from .base import BaseGraph
from .views.undirected import UndirectedEdge, UndirectedEdgeView
from .views.vertex import VertexView


class UndirectedGraph[VertT, VertLabelT, EdgeSymbolT](BaseGraph[VertT, UndirectedEdge[VertT], VertLabelT, EdgeSymbolT], edge_view=UndirectedEdgeView):
    vertices: VertexView[VertT, UndirectedEdge[VertT], VertLabelT, EdgeSymbolT]
    edges: UndirectedEdgeView[VertT, VertLabelT, EdgeSymbolT]
