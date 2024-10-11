from .directed import DirectedWalk


def test_directed_path() -> None:
    walk = DirectedWalk.from_vertex_list('a', 'b', 'c', 'd')
    assert list(walk.iter_vertices()) == list('abcd')


def test_directed_path_add() -> None:
    walk1 = DirectedWalk.from_vertex_list('a', 'b')
    walk2 = DirectedWalk.from_vertex_list('b', 'c')
    walk3 = DirectedWalk.from_vertex_list('a', 'b', 'c')
    assert walk1 + walk2 == walk3
