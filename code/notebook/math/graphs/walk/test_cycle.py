from .cycle import are_closed, is_cycle, remove_cycles
from .directed import DirectedWalk
from .undirected import UndirectedWalk


def test_is_cycle_trivial() -> None:
    walk = DirectedWalk.from_vertex_list('a')
    assert not is_cycle(walk)


def test_is_cycle_loop() -> None:
    walk = DirectedWalk.from_vertex_list('a', 'a')
    assert is_cycle(walk)


def test_is_cycle_directed_opposite() -> None:
    walk = DirectedWalk.from_vertex_list('a', 'b', 'a')
    assert is_cycle(walk)


def test_is_cycle_undirected_opposite() -> None:
    walk = UndirectedWalk.from_vertex_list('a', 'b', 'a')
    assert not is_cycle(walk)


def test_is_cycle_repeated() -> None:
    walk = DirectedWalk.from_vertex_list('a', 'b', 'c', 'a', 'd', 'c', 'a')
    assert are_closed(walk)
    assert not is_cycle(walk)


def test_cycle_removal_trivial() -> None:
    source = DirectedWalk.from_vertex_list('a')
    expected = source
    assert remove_cycles(source) == expected


def test_cycle_removal_noop() -> None:
    source = DirectedWalk.from_vertex_list('a', 'b', 'c')
    expected = source
    assert remove_cycles(source) == expected


def test_cycle_removal_loop() -> None:
    source = DirectedWalk.from_vertex_list('a', 'a')
    expected = DirectedWalk.from_vertex_list('a')
    assert remove_cycles(source) == expected


def test_cycle_removal_single_cycle() -> None:
    source = DirectedWalk.from_vertex_list('a', 'b', 'c', 'a', 'd', 'c')
    expected = DirectedWalk.from_vertex_list('a', 'd', 'c')
    assert remove_cycles(source) == expected


def test_cycle_removal_multiple_cycles() -> None:
    source = DirectedWalk.from_vertex_list('a', 'b', 'c', 'a', 'd', 'c', 'd', 'e')
    expected = DirectedWalk.from_vertex_list('a', 'd', 'e')
    assert remove_cycles(source) == expected
