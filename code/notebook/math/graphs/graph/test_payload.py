import pytest

from ..exceptions import MissingVertexError
from .payload import GraphPayload


def test_add_vertex_success() -> None:
    payload = GraphPayload[int, set[int], None, None]()
    payload.set_vertex(3)
    assert payload.has_vertex(3)


def test_remove_vertex_success() -> None:
    payload = GraphPayload[int, set[int], None, None]()
    payload.set_vertex(3)
    payload.remove_vertex(3)
    assert not payload.has_vertex(3)


def test_remove_vertex_failure_nonexisting() -> None:
    payload = GraphPayload[int, set[int], None, None]()

    with pytest.raises(MissingVertexError):
        payload.remove_vertex(3)


def test_get_labeled_vertices() -> None:
    payload = GraphPayload[int, set[int], str, None](default_vertex_label='')
    payload.set_vertex(3, '3')
    assert [tuple(lv) for lv in payload.get_labeled_vertices()] == [(3, '3')]


def test_add_edge_success() -> None:
    payload = GraphPayload[int, set[int], None, None]()
    payload.set_vertex(3)
    payload.set_vertex(4)
    payload.set_edge({3, 4})
    assert payload.has_edge({3, 4})


def test_remove_vertex_of_edge() -> None:
    payload = GraphPayload[int, set[int], None, None]()
    payload.set_vertex(3)
    payload.set_vertex(4)
    payload.set_edge({3, 4})
    payload.remove_vertex(3)
    assert not payload.has_edge({3, 4})


def test_get_labeled_edges() -> None:
    payload = GraphPayload[int, set[int], None, str](default_edge_label='')
    payload.set_vertex(3)
    payload.set_vertex(4)
    payload.set_edge({3, 4}, 'a')
    assert [tuple(lv) for lv in payload.get_labeled_edges()] == [({3, 4}, 'a')]
