from typing import TYPE_CHECKING

from ...matrices.matrix import ISemiringMatrix, MinPlusMatrix
from ...rings.tropical import MinPlusFloat
from ...rings.types import ISemiring
from ..exceptions import GraphWalkError


if TYPE_CHECKING:
    from ..graph import DirectedGraph


def get_adjacency_matrix[N: ISemiring, T: ISemiringMatrix, VertLabelT](cls: type[T], graph: DirectedGraph[int, VertLabelT, N]) -> T:
    n = len(graph.vertices)
    result = cls.zeros(n)

    for edge, label in graph.edges.get_labeled():
        result[edge] = label

    return result


def get_min_walk_weights[VertLabelT](graph: DirectedGraph[int, VertLabelT, float], max_length: int) -> MinPlusMatrix:
    if max_length < 1:
        raise GraphWalkError(f'Expected a positive max length, but got {max_length}')

    mat = MinPlusMatrix.zeros(len(graph.vertices))

    for edge, label in graph.edges.get_labeled():
        mat[edge] = MinPlusFloat(label)

    result = mat

    for _ in range(max_length - 1):
        result @= mat

    return result
