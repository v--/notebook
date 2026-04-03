from .....graphs.graph import DirectedEdge, DirectedGraph
from ...structure import HolStructure
from .signature import DIRECTED_GRAPH_SIGNATURE


class DirectedGraphStructure[VertT](HolStructure[VertT | DirectedEdge[VertT]]):
    def __init__(self, graph: DirectedGraph[VertT]) -> None:
        self.signature = DIRECTED_GRAPH_SIGNATURE
        self.sort_universes = {
            DIRECTED_GRAPH_SIGNATURE.get_sort_symbol('vert'): set(graph.vertices),
            DIRECTED_GRAPH_SIGNATURE.get_sort_symbol('arc'): set(graph.edges),
        }

        self.interpretation = {
            DIRECTED_GRAPH_SIGNATURE.get_nonlogical_constant_symbol('src'): lambda edge: edge.src,
            DIRECTED_GRAPH_SIGNATURE.get_nonlogical_constant_symbol('dest'): lambda edge: edge.dest,
        }
