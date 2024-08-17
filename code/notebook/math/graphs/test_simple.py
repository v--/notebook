import pytest

from .generalized import ArcCardinalityError
from .simple import DirectedGraph, UndirectedGraph


def test_directed_vertices() -> None:
    graph: DirectedGraph[str, None, None] = DirectedGraph()
    assert 'a' not in graph.vertices
    graph.vertices.add('a')
    assert 'a' in graph.vertices


def test_directed_arcs() -> None:
    graph: DirectedGraph[str, None, None] = DirectedGraph()
    assert 'a' not in graph.vertices

    graph.arcs.add('a', 'b')
    assert 'a' in graph.vertices
    assert 'b' in graph.vertices
    assert ('a', 'b') in graph.arcs

    graph.vertices.remove('a')
    assert ('a', 'b') not in graph.arcs


def test_undirected_arcs() -> None:
    graph: UndirectedGraph[str, None, None] = UndirectedGraph()
    assert 'a' not in graph.vertices

    edge = frozenset(['a', 'b'])
    graph.edges.add(edge)
    assert 'a' in graph.vertices
    assert 'b' in graph.vertices
    assert edge in graph.edges

    graph.vertices.remove('a')
    assert edge not in graph.edges


def test_empty_undirected_arc() -> None:
    graph: UndirectedGraph[str, None, None] = UndirectedGraph()

    with pytest.raises(ArcCardinalityError):
        graph.edges.add(frozenset())


def test_undirected_arcs_invalid_size() -> None:
    graph: UndirectedGraph[str, None, None] = UndirectedGraph()

    with pytest.raises(ArcCardinalityError):
        graph.edges.add(frozenset(['a', 'b', 'c']))
