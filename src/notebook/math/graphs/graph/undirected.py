from typing import TYPE_CHECKING

from .base import BaseGraph
from .views.undirected import UndirectedEdge, UndirectedEdgeView


if TYPE_CHECKING:
    from .views.vertex import VertexView


class UndirectedGraph[VertT, VertLabelT = None, EdgeSymbolT = None](BaseGraph[VertT, UndirectedEdge[VertT], VertLabelT, EdgeSymbolT], edge_view=UndirectedEdgeView):
    vertices: VertexView[VertT, UndirectedEdge[VertT], VertLabelT, EdgeSymbolT]
    edges: UndirectedEdgeView[VertT, VertLabelT, EdgeSymbolT]
