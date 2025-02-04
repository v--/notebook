import itertools
from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta

from ...exceptions import UnreachableException
from ..graphs.complete import max_edge_count
from ..graphs.graph import UndirectedGraph
from ..graphs.subgraphs import enumerate_fixed_order_subgraphs, max_fixed_order_subgraph_count
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
                colored_graph.edges[i, j] = next(it)

        yield colored_graph


def enumerate_sized_colored_subgraphs(graph: EdgeColoredGraph, sizes: Collection[int]) -> Iterable[tuple[ColorType, EdgeColoredGraph]]:
    for (k, s_k) in enumerate(sizes):
        for subgraph in enumerate_fixed_order_subgraphs(graph, order=s_k):
            yield k, subgraph


@dataclass(frozen=True)
class ExhaustiveRamseyComputationBounds:
    result_max: int
    max_edge_count: int
    max_subgraphs_per_coloring: Mapping[int, int]


def naive_ramsey_computation_bounds(s: int, t: int, *rest: int) -> ExhaustiveRamseyComputationBounds:
    result_bound = ramsey_upper_bound(s, t, *rest)
    sizes = [s, t, *rest]

    return ExhaustiveRamseyComputationBounds(
        result_max=result_bound,
        max_edge_count=max_edge_count(result_bound - 1),
        max_subgraphs_per_coloring={s_k: max_fixed_order_subgraph_count(result_bound - 1, s_k) for s_k in sizes}
    )


@dataclass(frozen=True)
class ExhaustiveRamseyComputationState:
    sizes: Collection[int]

    run_time: timedelta

    result: int | None
    colorings_traversed: int
    subgraphs_traversed: int


# This approach is discussed in rem:estimating_ramsey_numbers in the monograph.
def compute_ramsey_number_exhaustively_streaming(s: int, t: int, *rest: int, batch_size: int | None = None) -> Iterable[ExhaustiveRamseyComputationState]:
    bounds = naive_ramsey_computation_bounds(s, t, *rest)
    sizes = [s, t, *rest]

    if bounds.result_max <= 2:
        yield ExhaustiveRamseyComputationState(
            sizes=sizes,
            result=bounds.result_max,
            run_time=timedelta(),
            colorings_traversed=0,
            subgraphs_traversed=0
        )

        return

    start = datetime.now()
    checkpoint = 0
    subgraphs_traversed = 0
    colorings_traversed = 0

    for n in range(bounds.result_max - 1, min(sizes) - 1, -1):
        for colored_graph in enumerate_complete_graph_coloring(n=n, r=len(sizes)):
            colorings_traversed += 1

            for k, subgraph in enumerate_sized_colored_subgraphs(colored_graph, sizes):
                subgraphs_traversed += 1

                if batch_size is not None and subgraphs_traversed - checkpoint >= batch_size:
                    checkpoint = subgraphs_traversed

                    yield ExhaustiveRamseyComputationState(
                        sizes=sizes,
                        colorings_traversed=colorings_traversed,
                        subgraphs_traversed=subgraphs_traversed,
                        run_time=datetime.now() - start,
                        result=None
                    )

                if all(label == k for _, label in subgraph.edges.get_labeled()):
                    break
            else:
                yield ExhaustiveRamseyComputationState(
                    sizes=sizes,
                    colorings_traversed=colorings_traversed,
                    subgraphs_traversed=subgraphs_traversed,
                    run_time=datetime.now() - start,
                    result=n + 1
                )

                return

    raise UnreachableException


def compute_ramsey_number_exhaustively(s: int, t: int, *rest: int) -> ExhaustiveRamseyComputationState:
    for state in compute_ramsey_number_exhaustively_streaming(s, t, *rest, batch_size=None):
        if state.result is not None:
            return state

    raise UnreachableException
