from ...matrices.matrix import ISemiringMatrix, MinPlusMatrix
from ...rings.arithmetic import ISemiring
from ...rings.tropical import MinPlusFloat
from ..graph import DirectedGraph


def get_adjacency_matrix[N: ISemiring, T: ISemiringMatrix, VertLabelT](cls: type[T], graph: DirectedGraph[int, VertLabelT, N]) -> T:
    n = len(graph.vertices)
    result = cls.zeros(n)

    for edge, label in graph.edges.get_labeled():
        result[edge] = label

    return result


def get_min_walk_weights[VertLabelT](graph: DirectedGraph[int, VertLabelT, float], max_length: int) -> MinPlusMatrix:
    assert max_length >= 1

    mat = MinPlusMatrix.zeros(len(graph.vertices))

    for edge, label in graph.edges.get_labeled():
        mat[edge] = MinPlusFloat(label)

    result = mat

    for _ in range(max_length - 1):
        result @= mat

    return result
