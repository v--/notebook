from typing import TYPE_CHECKING

from .base import BaseGraph
from .views.directed_multi import DirectedMultiedge, DirectedMultiedgeView


if TYPE_CHECKING:
    from .views.vertex import VertexView


class DirectedMultigraph[VertT, VertLabelT, EdgeLabelT](BaseGraph[VertT, DirectedMultiedge[VertT], VertLabelT, EdgeLabelT], edge_view=DirectedMultiedgeView):
    vertices: VertexView[VertT, DirectedMultiedge[VertT], VertLabelT, EdgeLabelT]
    edges: DirectedMultiedgeView[VertT, VertLabelT, EdgeLabelT]
