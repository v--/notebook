from .directed import DirectedGraph


def test_can_add_vertices():
    graph = DirectedGraph()

    assert 1 not in graph.vertices
    graph.vertices.add(1)
    assert 1 in graph.vertices
    assert graph.vertices[1] is None


def test_can_add_vertices_with_attr():
    graph = DirectedGraph()

    assert 1 not in graph.vertices
    graph.vertices[1] = 'test'
    assert graph.vertices[1] == 'test'


def test_can_add_edges():
    graph = DirectedGraph()

    assert 1 not in graph.vertices
    assert 2 not in graph.vertices

    graph.arcs.add(1, 2)
    assert 1 in graph.vertices
    assert 2 in graph.vertices
    assert (1, 2) in graph.arcs


def test_can_add_edges_with_attr():
    graph = DirectedGraph()

    graph.arcs[1, 2] = 'test'
    assert graph.arcs[1, 2] == 'test'
