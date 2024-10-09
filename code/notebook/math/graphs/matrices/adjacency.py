from ...linalg.matrix import Matrix, fill
from ...opt.tropical import MinPlusFloat
from ..graph import DirectedGraph


def get_adjacency_matrix[N: (int, float, complex), VertLabelT](graph: DirectedGraph[int, VertLabelT, N], dtype: type[N] = int, blank: N = 0) -> Matrix[N]:
    n = len(graph.vertices)
    result = fill(n, dtype=dtype, value=blank)

    for edge, label in graph.edges.get_labeled():
        result[edge] = dtype(label)

    return result


def get_min_walk_weights[VertLabelT](graph: DirectedGraph[int, VertLabelT, float], max_length: int) -> Matrix[float]:
    assert max_length >= 1
    matrix = get_adjacency_matrix(graph, dtype=MinPlusFloat, blank=float('inf'))
    result = matrix

    for _ in range(max_length - 1):
        result @= matrix

    return result
