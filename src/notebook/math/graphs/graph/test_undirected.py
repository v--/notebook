from .undirected import UndirectedGraph


def test_contains_opposite_edge() -> None:
    graph = UndirectedGraph[int, None, None]()
    graph.edges.add(3, 4)
    assert (4, 3) in graph.edges
