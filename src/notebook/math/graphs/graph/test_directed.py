from .directed import DirectedEdge, DirectedGraph


def test_add_entire_edge() -> None:
    graph = DirectedGraph[int, None, None]()
    graph.edges.add(DirectedEdge(3, 4))
    assert DirectedEdge(3, 4) in graph.edges


def test_add_entire_edge_with_label() -> None:
    graph = DirectedGraph[int, None, str]()
    graph.edges[DirectedEdge(3, 4)] = 'label'
    assert graph.edges[(3, 4)] == 'label'


def test_add_edge_tuple() -> None:
    graph = DirectedGraph[int, None, None]()
    graph.edges.add((3, 4))
    assert (3, 4) in graph.edges


def test_add_edge_two_vertices() -> None:
    graph = DirectedGraph[int, None, None]()
    graph.edges.add(3, 4)
    assert (3, 4) in graph.edges


def test_add_edge_two_vertices_with_label() -> None:
    graph = DirectedGraph[int, None, str]()
    graph.edges[(3, 4)] = 'label'
    assert graph.edges[(3, 4)] == 'label'
