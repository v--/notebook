import pytest

from ..exceptions import EdgeExistsError, MissingVertexError, VertexExistsError
from .payload import GraphPayload


def test_add_vertex_success() -> None:
    payload = GraphPayload[int, set[int], None, None]()
    payload.add_vertex(3)
    assert payload.has_vertex(3)


def test_add_vertex_failure_duplicate() -> None:
    payload = GraphPayload[int, set[int], None, None]()
    payload.add_vertex(3)

    with pytest.raises(VertexExistsError):
        payload.add_vertex(3)


def test_remove_vertex_success() -> None:
    payload = GraphPayload[int, set[int], None, None]()
    payload.add_vertex(3)
    payload.remove_vertex(3)
    assert not payload.has_vertex(3)


def test_remove_vertex_failure_nonexisting() -> None:
    payload = GraphPayload[int, set[int], None, None]()

    with pytest.raises(MissingVertexError):
        payload.remove_vertex(3)


def test_get_labeled_vertices() -> None:
    payload = GraphPayload[int, set[int], str, None]()
    payload.add_vertex(3, '3')
    assert [tuple(lv) for lv in payload.get_labeled_vertices()] == [(3, '3')]


def test_add_edge_success() -> None:
    payload = GraphPayload[int, set[int], None, None]()
    payload.add_vertex(3)
    payload.add_vertex(4)
    payload.add_edge({3, 4})
    assert payload.has_edge({3, 4})


def test_add_edge_failure() -> None:
    payload = GraphPayload[int, set[int], None, None]()

    with pytest.raises(MissingVertexError):
        payload.add_edge({3, 4})


def test_remove_vertex_failure_edge() -> None:
    payload = GraphPayload[int, set[int], None, None]()
    payload.add_vertex(3)
    payload.add_vertex(4)
    payload.add_edge({3, 4})

    with pytest.raises(EdgeExistsError):
        payload.remove_vertex(3)


def test_get_labeled_edges() -> None:
    payload = GraphPayload[int, set[int], None, str]()
    payload.add_vertex(3)
    payload.add_vertex(4)
    payload.add_edge({3, 4}, 'a')
    assert [tuple(lv) for lv in payload.get_labeled_edges()] == [({3, 4}, 'a')]
