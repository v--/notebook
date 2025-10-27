from .base import BaseGraph
from .views.directed_multi import DirectedMultiedge, DirectedMultiedgeView
from .views.vertex import VertexView


class DirectedMultigraph[VertT, VertLabelT, EdgeSymbolT](BaseGraph[VertT, DirectedMultiedge[VertT], VertLabelT, EdgeSymbolT], edge_view=DirectedMultiedgeView):
    vertices: VertexView[VertT, DirectedMultiedge[VertT], VertLabelT, EdgeSymbolT]
    edges: DirectedMultiedgeView[VertT, VertLabelT, EdgeSymbolT]
