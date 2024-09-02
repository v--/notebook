
from ..combinatorics.binomial import choose
from .generalized import BaseVertType
from .simple import UndirectedGraph


def edgeless_graph(n: int) -> UndirectedGraph[int, None, None]:
    result = UndirectedGraph[int, None, None]()

    for i in range(n):
        result.vertices.add(i)

    return result


def complete_graph(n: int) -> UndirectedGraph[int, None, None]:
    result = UndirectedGraph[int, None, None]()

    for i in range(n):
        for j in range(i):
            result.edges.add(i, j)

    return result


def max_edge_count(n: int) -> int:
    return choose(n, 2)


def is_complete[VertT: BaseVertType, VertLabelT, ArcLabelT](
    graph: UndirectedGraph[VertT, VertLabelT, ArcLabelT]
) -> bool:
    return len(graph.edges) == max_edge_count(len(graph.vertices))
