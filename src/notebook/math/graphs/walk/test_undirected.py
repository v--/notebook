from .undirected import UndirectedWalk


def test_undirected_path() -> None:
    walk = UndirectedWalk.from_vertex_list('a', 'b', 'c', 'd')
    assert list(walk.iter_vertices()) == list('abcd')
