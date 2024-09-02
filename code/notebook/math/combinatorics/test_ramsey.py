from .ramsey import compute_ramsey_number_exhaustively, naive_ramsey_computation_bounds, ramsey_upper_bound, compute_ramsey_number_exhaustively_streaming


def test_ramsey_upper_bound() -> None:
    assert ramsey_upper_bound(1, 5) == 1
    assert ramsey_upper_bound(2, 5) == 5
    assert ramsey_upper_bound(3, 5) == 15
    assert ramsey_upper_bound(4, 5) == 35
    assert ramsey_upper_bound(5, 5) == 70

    assert ramsey_upper_bound(3, 3) == 6
    assert ramsey_upper_bound(3, 3, 2) == 6
    assert ramsey_upper_bound(3, 3, 3) == 21


def test_naive_ramsey_computation_bounds() -> None:
    bounds = naive_ramsey_computation_bounds(3, 3)
    assert bounds.result_max == 6
    assert bounds.max_edge_count == 10
    assert bounds.max_subgraphs_per_coloring == {3: 10}

    bounds = naive_ramsey_computation_bounds(3, 3, 2)
    assert bounds.result_max == 6
    assert bounds.max_edge_count == 10
    assert bounds.max_subgraphs_per_coloring == {2: 10, 3: 10}

    bounds = naive_ramsey_computation_bounds(3, 4)
    assert bounds.result_max == 10
    assert bounds.max_edge_count == 36
    assert bounds.max_subgraphs_per_coloring == {3: 84, 4: 126}

    bounds = naive_ramsey_computation_bounds(3, 3, 3)
    assert bounds.result_max == 21
    assert bounds.max_edge_count == 190
    assert bounds.max_subgraphs_per_coloring == {3: 1140}


def test_compute_ramsey_number_exhaustively() -> None:
    state = compute_ramsey_number_exhaustively(1, 3)
    assert state.result == 1

    state = compute_ramsey_number_exhaustively(2, 2)
    assert state.result == 2

    state = compute_ramsey_number_exhaustively(2, 3)
    assert state.result == 3
    assert state.colorings_traversed == 2
    assert state.subgraphs_traversed == 2

    state = compute_ramsey_number_exhaustively(3, 3)
    assert state.result == 6
    assert state.colorings_traversed == 221
    assert state.subgraphs_traversed == 729
