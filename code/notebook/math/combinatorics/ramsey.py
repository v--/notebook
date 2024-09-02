import itertools
from collections.abc import Collection, Iterable
from typing import NamedTuple

from ...exceptions import UnreachableException
from ..graphs.simple import UndirectedGraph
from ..graphs.subgraphs import enumerate_fixed_order_subgraphs
from .binomial import choose


ColorType = int
EdgeColoredGraph = UndirectedGraph[int, None, ColorType]


def ramsey_upper_bound(s: int, t: int, *rest: int) -> int:
    base = choose(s + t - 2, min(s, t) - 1)

    if len(rest) == 0:
        return base

    return ramsey_upper_bound(base, *rest)


def enumerate_edge_coloring_sequences(n: int, r: int) -> Iterable[Collection[int]]:
    colors = list(range(r))
    m = choose(n, 2)
    yield from itertools.product(*([colors] * m))


def enumerate_complete_graph_coloring(n: int, r: int) -> Iterable[EdgeColoredGraph]:
    for coloring in enumerate_edge_coloring_sequences(n, r):
        colored_graph = UndirectedGraph[int, None, ColorType]()
        it = iter(coloring)

        for i in range(n):
            for j in range(i):
                colored_graph.edges.add(i, j, next(it))

        yield colored_graph


def enumerate_sized_colored_subgraphs(graph: EdgeColoredGraph, sizes: Collection[int]) -> Iterable[tuple[ColorType, EdgeColoredGraph]]:
    for (k, s_k) in enumerate(sizes):
        for subgraph in enumerate_fixed_order_subgraphs(graph, order=s_k):
            yield k, subgraph


class RamseyNumberComputation(NamedTuple):
    result: int
    subgraphs_traversed: int
    args: Collection[int]


# This approach is discussed in rem:estimating_ramsey_numbers in the monograph.
def compute_ramsey_naive(s: int, t: int, *rest: int) -> RamseyNumberComputation:
    bound = ramsey_upper_bound(s, t, *rest)
    sizes = [s, t, *rest]

    if bound == 1:
        return RamseyNumberComputation(args=sizes, result=1, subgraphs_traversed=0)

    traversed = 0

    for n in range(bound - 1, min(sizes) - 1, -1):
        for colored_graph in enumerate_complete_graph_coloring(n=n, r=len(sizes)):
            for k, subgraph in enumerate_sized_colored_subgraphs(colored_graph, sizes):
                traversed += 1

                if all(subgraph.edges.get_label(edge) == k for edge in subgraph.edges):
                    break
            else:
                return RamseyNumberComputation(args=sizes, result=n + 1, subgraphs_traversed=traversed)

    raise UnreachableException
