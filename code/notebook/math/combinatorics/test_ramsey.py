import itertools
from collections.abc import Sequence

from ...support.pytest import pytest_parametrize_kwargs
from .ramsey import (
    ExhaustiveRamseyComputationBounds,
    compute_ramsey_number_exhaustively,
    compute_ramsey_number_exhaustively_streaming,
    naive_ramsey_computation_bounds,
    ramsey_upper_bound,
)


@pytest_parametrize_kwargs(
    dict(sizes=[1, 5], expected=1),
    dict(sizes=[2, 5], expected=5),
    dict(sizes=[3, 5], expected=15),
    dict(sizes=[4, 5], expected=35),
    dict(sizes=[5, 5], expected=70),
    dict(sizes=[3, 3], expected=6),
    dict(sizes=[3, 3, 2], expected=6),
    dict(sizes=[3, 3, 3], expected=21)
)
def test_ramsey_upper_bound_binary(sizes: Sequence[int], expected: int) -> None:
    assert ramsey_upper_bound(*sizes) == expected

@pytest_parametrize_kwargs(
    dict(
        sizes=[3, 3],
        expected=ExhaustiveRamseyComputationBounds(
            result_max=6,
            max_edge_count=10,
            max_subgraphs_per_coloring={3: 10}
        )
    ),

    dict(
        sizes=[3, 3, 2],
        expected=ExhaustiveRamseyComputationBounds(
            result_max=6,
            max_edge_count=10,
            max_subgraphs_per_coloring={2: 10, 3: 10}
        )
    ),

    dict(
        sizes=[3, 4],
        expected=ExhaustiveRamseyComputationBounds(
            result_max=10,
            max_edge_count=36,
            max_subgraphs_per_coloring={3: 84, 4: 126}
        )
    ),

    dict(
        sizes=[3, 3, 3],
        expected=ExhaustiveRamseyComputationBounds(
            result_max=21,
            max_edge_count=190,
            max_subgraphs_per_coloring={3: 1140}
        )
    )
)
def test_naive_ramsey_computation_bounds(
    sizes: Sequence[int],
    expected: ExhaustiveRamseyComputationBounds
) -> None:
    bounds = naive_ramsey_computation_bounds(*sizes)
    assert bounds == expected


@pytest_parametrize_kwargs(
    dict(sizes=[1, 3], result=1, colorings_traversed=0,   subgraphs_traversed=0),
    dict(sizes=[2, 2], result=2, colorings_traversed=0,   subgraphs_traversed=0),
    dict(sizes=[2, 3], result=3, colorings_traversed=2,   subgraphs_traversed=2),
    dict(sizes=[3, 3], result=6, colorings_traversed=221, subgraphs_traversed=729),
)
def test_compute_ramsey_number_exhaustively(
    sizes: Sequence[int],
    result: int,
    colorings_traversed: int,
    subgraphs_traversed: int
) -> None:
    state = compute_ramsey_number_exhaustively(*sizes)
    assert state.result == result
    assert state.colorings_traversed == colorings_traversed
    assert state.subgraphs_traversed == subgraphs_traversed


@pytest_parametrize_kwargs(
    dict(sizes=[3, 4], batch_size=10, batch_count=3, expected_colorings_traversed=60)
)
def test_compute_ramsey_number_exhaustively_streaming(
    sizes: Sequence[int],
    batch_size: int,
    batch_count: int,
    expected_colorings_traversed: int
) -> None:
    stream = compute_ramsey_number_exhaustively_streaming(*sizes, batch_size=batch_size)
    total_colorings_traversed = 0

    for batch in itertools.islice(stream, batch_count):
        total_colorings_traversed += batch.colorings_traversed

    assert total_colorings_traversed == expected_colorings_traversed
