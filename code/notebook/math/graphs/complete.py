
from ..combinatorics.binomial import choose
from .graph import UndirectedGraph


def edgeless_graph(n: int) -> UndirectedGraph[int, None, None]:
    result = UndirectedGraph[int, None, None]()

    for i in range(n):
        result.vertices.add(i)

    return result


def complete_graph(n: int) -> UndirectedGraph[int, None, None]:
    result = UndirectedGraph[int, None, None]()

    for i in range(n):
        result.vertices.add(i)

        for j in range(i):
            result.edges.add(i, j)

    return result


def max_edge_count(n: int) -> int:
    return choose(n, 2)


def is_complete[VertT, VertLabelT, EdgeLabelT](
    graph: UndirectedGraph[VertT, VertLabelT, EdgeLabelT]
) -> bool:
    return len(graph.edges) == max_edge_count(len(graph.vertices))
