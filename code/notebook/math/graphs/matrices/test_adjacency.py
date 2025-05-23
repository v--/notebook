from ...matrices.matrix import IntMatrix, MinPlusMatrix
from ...rings.tropical import MinPlusFloat
from ..graph import DirectedGraph
from .adjacency import get_adjacency_matrix, get_min_walk_weights


def test_get_adjacency_matrix() -> None:
    graph: DirectedGraph[int, None, int] = DirectedGraph()

    graph.edges[0, 1] = 3
    graph.edges[0, 2] = 2
    graph.edges[0, 3] = 4
    graph.edges[1, 3] = 1
    graph.edges[2, 3] = 1

    assert get_adjacency_matrix(IntMatrix, graph) == IntMatrix.from_rows([
        [0, 3, 2, 4],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ])


def test_get_min_walk_weight() -> None:
    graph: DirectedGraph[int, None, float] = DirectedGraph()

    graph.edges[0, 1] = 3.0
    graph.edges[0, 2] = 2.0
    graph.edges[0, 3] = 4.0
    graph.edges[1, 3] = 1.0
    graph.edges[2, 3] = 1.0

    min_walk_weights = MinPlusMatrix.zeros(len(graph.vertices))
    min_walk_weights[0, 3] = MinPlusFloat(3.0)

    assert get_min_walk_weights(graph, max_length=2) == min_walk_weights
