from .cycle import is_closed, is_cycle, remove_cycles
from .directed import DirectedWalk
from .undirected import UndirectedWalk


def test_is_cycle_trivial() -> None:
    walk = DirectedWalk.path('a')
    assert not is_cycle(walk)


def test_is_cycle_loop() -> None:
    walk = DirectedWalk.path('a', 'a')
    assert is_cycle(walk)


def test_is_cycle_directed_opposite() -> None:
    walk = DirectedWalk.path('a', 'b', 'a')
    assert is_cycle(walk)


def test_is_cycle_undirected_opposite() -> None:
    edge = frozenset(['a', 'b'])
    walk = UndirectedWalk('a', [edge, edge])
    assert not is_cycle(walk)


def test_is_cycle_repeated() -> None:
    walk = DirectedWalk.path('a', 'b', 'c', 'a', 'd', 'c', 'a')
    assert is_closed(walk)
    assert not is_cycle(walk)


def test_cycle_removal_trivial() -> None:
    source = DirectedWalk.path('a')
    expected = source
    assert remove_cycles(source) == expected


def test_cycle_removal_noop() -> None:
    source = DirectedWalk.path('a', 'b', 'c')
    expected = source
    assert remove_cycles(source) == expected


def test_cycle_removal_loop() -> None:
    source = DirectedWalk.path('a', 'a')
    expected = DirectedWalk.path('a')
    assert remove_cycles(source) == expected


def test_cycle_removal_single_cycle() -> None:
    source = DirectedWalk.path('a', 'b', 'c', 'a', 'd', 'c')
    expected = DirectedWalk.path('a', 'd', 'c')
    assert remove_cycles(source) == expected


def test_cycle_removal_multiple_cycles() -> None:
    source = DirectedWalk.path('a', 'b', 'c', 'a', 'd', 'c', 'd', 'e')
    expected = DirectedWalk.path('a', 'd', 'e')
    assert remove_cycles(source) == expected
