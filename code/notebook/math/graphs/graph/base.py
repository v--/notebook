import functools
from collections.abc import Callable, Collection
from typing import Any, Self, overload

from .payload import GraphPayload
from .views.base_edge import BaseEdgeView
from .views.vertex import VertexView


class GraphMeta[VertT, EdgeT: Collection, VertLabelT, EdgeSymbolT](type):
    payload_class: type[GraphPayload]
    vertex_view_class: type[VertexView]
    edge_view_class: type[BaseEdgeView]

    def __new__[T: GraphMeta](
        meta: type[T],
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        payload: type[GraphPayload] = GraphPayload,
        vertex_view: type[VertexView] = VertexView,
        edge_view: type[BaseEdgeView] = BaseEdgeView,
    ) -> T:
        attrs['payload_class'] = payload
        attrs['vertex_view_class'] = vertex_view
        attrs['edge_view_class'] = edge_view
        return type.__new__(meta, name, bases, attrs)

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        result = super().__call__(*args, **kwargs)
        result.clone_initial = functools.partial(cls.__call__, *args, **kwargs)
        return result


class BaseGraph[VertT, EdgeT: Collection, VertLabelT, EdgeSymbolT](metaclass=GraphMeta):
    clone_initial: Callable[[], Self]
    vertices: VertexView
    edges: BaseEdgeView

    @overload
    def __init__(self, *, default_vertex_label: VertLabelT, default_edge_label: EdgeSymbolT) -> None: ...
    @overload
    def __init__(self: 'BaseGraph[VertT, EdgeT, VertLabelT, None]', *, default_vertex_label: VertLabelT, default_edge_label: None = None) -> None: ...
    @overload
    def __init__(self: 'BaseGraph[VertT, EdgeT, None, EdgeSymbolT]', *, default_vertex_label: None = None, default_edge_label: EdgeSymbolT) -> None: ...
    @overload
    def __init__(self: 'BaseGraph[VertT, EdgeT, None, None]', *, default_vertex_label: None = None, default_edge_label: None = None) -> None: ...
    def __init__(self, *, default_vertex_label: VertLabelT | None = None, default_edge_label: EdgeSymbolT | None = None) -> None:
        cls = type(self)
        payload = cls.payload_class(default_vertex_label=default_vertex_label, default_edge_label=default_edge_label)
        self.vertices = cls.vertex_view_class(payload)
        self.edges = cls.edge_view_class(payload)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseGraph) and self.vertices == other.vertices and self.edges == other.edges

    def clone(self) -> Self:
        result = self.clone_initial()

        for vertex, label in self.vertices.get_labeled():
            result.vertices[vertex] = label

        for edge, label in self.edges.get_labeled():
            result.edges[edge] = label

        return result

    def induced(self, vertices: Collection[VertT]) -> Self:
        result = self.clone_initial()

        for vertex, label in self.vertices.get_labeled():
            if vertex in vertices:
                result.vertices[vertex] = label

        for edge, label in self.edges.get_labeled():
            if all(endpoint in vertices for endpoint in edge):
                result.edges[edge] = label

        return result
