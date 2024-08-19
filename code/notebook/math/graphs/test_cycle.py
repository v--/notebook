
from .cycle import is_closed, is_cycle, remove_cycles
from .multi import MultiEdge
from .walk import DirectedWalk, UndirectedWalk


def test_is_cycle_trivial() -> None:
    walk = DirectedWalk.simple('a')
    assert not is_cycle(walk)


def test_is_cycle_loop() -> None:
    walk = DirectedWalk.simple('a', 'a')
    assert is_cycle(walk)


def test_is_cycle_directed_opposite() -> None:
    walk = DirectedWalk.simple('a', 'b', 'a')
    assert is_cycle(walk)


def test_is_cycle_undirected_opposite() -> None:
    edge = frozenset(['a', 'b'])
    walk = UndirectedWalk('a', [edge, edge])
    assert not is_cycle(walk)


def test_is_cycle_multi_undirected_opposite() -> None:
    edge1 = MultiEdge('a', 'b')
    edge2 = MultiEdge('a', 'b')
    walk = UndirectedWalk('a', [edge1, edge2])
    assert is_cycle(walk)


def test_is_cycle_repeated() -> None:
    walk = DirectedWalk.simple('a', 'b', 'c', 'a', 'd', 'c', 'a')
    assert is_closed(walk)
    assert not is_cycle(walk)


def test_cycle_removal_trivial() -> None:
    source = DirectedWalk.simple('a')
    expected = source
    assert remove_cycles(source) == expected


def test_cycle_removal_noop() -> None:
    source = DirectedWalk.simple('a', 'b', 'c')
    expected = source
    assert remove_cycles(source) == expected


def test_cycle_removal_loop() -> None:
    source = DirectedWalk.simple('a', 'a')
    expected = DirectedWalk.simple('a')
    assert remove_cycles(source) == expected


def test_cycle_removal_single_cycle() -> None:
    source = DirectedWalk.simple('a', 'b', 'c', 'a', 'd', 'c')
    expected = DirectedWalk.simple('a', 'd', 'c')
    assert remove_cycles(source) == expected


def test_cycle_removal_multiple_cycles() -> None:
    source = DirectedWalk.simple('a', 'b', 'c', 'a', 'd', 'c', 'd', 'e')
    expected = DirectedWalk.simple('a', 'd', 'e')
    assert remove_cycles(source) == expected
