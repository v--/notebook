import itertools
from collections.abc import Collection, Iterable

from ..combinatorics.binomial import choose
from .graph import UndirectedGraph


def max_fixed_order_subgraph_count(n: int, order: int) -> int:
    return choose(n, order)


def enumerate_fixed_order_subgraphs[VertT, VertLabelT, EdgeLabelT](
    graph: UndirectedGraph[VertT, VertLabelT, EdgeLabelT],
    order: int,
) -> Iterable[UndirectedGraph[VertT, VertLabelT, EdgeLabelT]]:
    for subset in itertools.combinations(graph.vertices, order):
        yield graph.induced(subset)


def max_subgraph_count(n: int) -> int:
    return sum(max_fixed_order_subgraph_count(n, k) for k in range(1, n)) + 1


def enumerate_subgraphs[VertT, VertLabelT, EdgeLabelT](
    graph: UndirectedGraph[VertT, VertLabelT, EdgeLabelT]
) -> Collection[UndirectedGraph[VertT, VertLabelT, EdgeLabelT]]:
    n = len(graph.vertices)

    result = list[UndirectedGraph[VertT, VertLabelT, EdgeLabelT]]()
    result.append(graph)

    if n == 1:
        return result

    for v in list(graph.vertices):
        subgraph = graph.clone()
        subgraph.vertices.remove(v, remove_edges=True)

        for subsubgraph in enumerate_subgraphs(subgraph):
            if subsubgraph not in result:
                result.append(subsubgraph)

    return result
