import itertools
from collections.abc import Collection, Iterable

from ..combinatorics.binomial import choose
from .generalized import BaseVertType
from .simple import UndirectedGraph


def max_fixed_order_subgraph_count(n: int, order: int) -> int:
    return choose(n, order)


def enumerate_fixed_order_subgraphs[VertT: BaseVertType, VertLabelT, ArcLabelT](
    graph: UndirectedGraph[VertT, VertLabelT, ArcLabelT],
    order: int,
) -> Iterable[UndirectedGraph[VertT, VertLabelT, ArcLabelT]]:
    for subset in set(itertools.combinations(list(graph.vertices), order)):
        yield graph.induced(subset)


def max_subgraph_count(n: int) -> int:
    return sum(max_fixed_order_subgraph_count(n, k) for k in range(1, n)) + 1


def enumerate_subgraphs[VertT: BaseVertType, VertLabelT, ArcLabelT](
    graph: UndirectedGraph[VertT, VertLabelT, ArcLabelT]
) -> Collection[UndirectedGraph[VertT, VertLabelT, ArcLabelT]]:
    n = len(graph.vertices)

    result = list[UndirectedGraph[VertT, VertLabelT, ArcLabelT]]()
    result.append(graph)

    if n == 1:
        return result

    for v in list(graph.vertices):
        subgraph = graph.dup()
        subgraph.vertices.remove(v)

        for subsubgraph in enumerate_subgraphs(subgraph):
            if subsubgraph not in result:
                result.append(subsubgraph)

    return result
