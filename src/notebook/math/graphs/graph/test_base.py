from .base import BaseGraph


def test_add_vertex_no_label() -> None:
    graph = BaseGraph[int, set[int], None, None]()
    graph.vertices.add(3)
    assert 3 in graph.vertices


def test_add_vertex_with_label() -> None:
    graph = BaseGraph[int, set[int], str, None]()
    graph.vertices[3] = '3'
    assert 3 in graph.vertices
    assert graph.vertices[3] == '3'


def test_remove_vertex_success() -> None:
    graph = BaseGraph[int, set[int], None, None]()
    graph.vertices.add(3)
    graph.vertices.remove(3)
    assert 3 not in graph.vertices


def test_get_labeled_vertices() -> None:
    graph = BaseGraph[int, set[int], str, None]()
    graph.vertices[3] = '3'
    assert [tuple(lv) for lv in graph.vertices.get_labeled()] == [(3, '3')]


def test_dup() -> None:
    graph = BaseGraph[int, set[int], str, None]()
    graph.vertices[2] = '2'
    graph.vertices[3] = '3'
    dup = graph.clone()
    assert graph == dup
