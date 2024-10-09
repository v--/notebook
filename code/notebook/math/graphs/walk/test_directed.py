from .directed import DirectedWalk


def test_directed_path() -> None:
    walk = DirectedWalk.path('a', 'b', 'c', 'd')
    assert list(walk.iter_vertices()) == list('abcd')


def test_directed_path_add() -> None:
    walk1 = DirectedWalk.path('a', 'b')
    walk2 = DirectedWalk.path('b', 'c')
    walk3 = DirectedWalk.path('a', 'b', 'c')
    assert walk1 + walk2 == walk3


def test_directed_trivial_path() -> None:
    walk = DirectedWalk.path('a')
    assert list(walk.iter_vertices()) == ['a']
