import itertools

from .walk import DirectedWalk, UndirectedWalk


def test_directed_path() -> None:
    walk = DirectedWalk.simple('a', 'b', 'c', 'd')
    assert list(walk.iter_vertices()) == list('abcd')


def test_directed_path_add() -> None:
    walk1 = DirectedWalk.simple('a', 'b')
    walk2 = DirectedWalk.simple('b', 'c')
    walk3 = DirectedWalk.simple('a', 'b', 'c')
    assert walk1 + walk2 == walk3


def test_directed_trivial_path() -> None:
    walk = DirectedWalk.simple('a')
    assert list(walk.iter_vertices()) == ['a']


def test_undirected_path() -> None:
    walk = UndirectedWalk('a', [('b', 'a'), ('b', 'c'), ('d', 'c')])
    assert list(walk.iter_vertices()) == list('abcd')


def test_undirected_trivial_path() -> None:
    walk = UndirectedWalk.simple('a')
    assert list(walk.iter_vertices()) == ['a']
