from .cycles import Cycle


def test_empty_cycle_decomposition():
    cycle: Cycle[int] = Cycle([])
    assert list(cycle.iter_decomposed()) == [cycle]


def test_unary_cycle_decomposition():
    cycle = Cycle([1])
    assert list(cycle.iter_decomposed()) == [Cycle([])]


def test_transposition_decomposition():
    cycle = Cycle([1, 2])
    assert list(cycle.iter_decomposed()) == [Cycle([1, 2])]


def test_long_cycle_decomposition():
    cycle = Cycle([1, 2, 3, 4])
    assert list(cycle.iter_decomposed()) == [Cycle([1, 2]), Cycle([1, 3]), Cycle([1, 4])]
