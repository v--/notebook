from ...linalg.matrix import Matrix, N, fill
from ...opt.tropical import MinPlusFloat
from ..generalized import VertLabelT
from ..simple import DirectedGraph


def get_adjacency_matrix(graph: DirectedGraph[int, VertLabelT, N], dtype: type[N] = int, blank: N = 0) -> Matrix[N]:
    n = len(graph.vertices)
    result = fill(n, dtype=dtype, value=blank)

    for arc in graph.arcs:
        src, dest = arc
        result[src, dest] = dtype(graph.arcs.get_label(arc))

    return result


def get_min_walk_weights(graph: DirectedGraph[int, VertLabelT, float], max_length: int) -> Matrix[float]:
    assert max_length >= 1
    matrix = get_adjacency_matrix(graph, dtype=MinPlusFloat, blank=float('inf'))
    result = matrix

    for _ in range(max_length - 1):
        result @= matrix

    return result
