from .undirected import UndirectedWalk


def test_undirected_path() -> None:
    walk = UndirectedWalk('a', [('b', 'a'), ('b', 'c'), ('d', 'c')])
    assert list(walk.iter_vertices()) == list('abcd')


def test_undirected_trivial_path() -> None:
    walk = UndirectedWalk.path('a')
    assert list(walk.iter_vertices()) == ['a']
