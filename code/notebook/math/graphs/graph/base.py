import functools
from collections.abc import Callable, Collection
from typing import Any, Self

from .payload import GraphPayload
from .views.base_edge import BaseEdgeView
from .views.vertex import VertexView


class GraphMeta[VertT, EdgeT: Collection, VertLabelT, EdgeLabelT](type):
    payload_class: type[GraphPayload]
    vertex_view_class: type[VertexView]
    edge_view_class: type[BaseEdgeView]

    def __new__[T: GraphMeta](
        meta: type[T],  # noqa: N804
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        payload: type[GraphPayload] = GraphPayload,
        vertex_view: type[VertexView] = VertexView,
        edge_view: type[BaseEdgeView] = BaseEdgeView,
    ) -> T:  # noqa: PYI019
        attrs['payload_class'] = payload
        attrs['vertex_view_class'] = vertex_view
        attrs['edge_view_class'] = edge_view
        return type.__new__(meta, name, bases, attrs)

    def __call__[T: GraphMeta](cls: T, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        result = super().__call__(*args, **kwargs)
        payload = cls.payload_class()
        result.vertices = cls.vertex_view_class(payload)
        result.edges = cls.edge_view_class(payload)
        result.reinit = functools.partial(cls.__call__, *args, **kwargs)
        return result


class BaseGraph[VertT, EdgeT: Collection, VertLabelT, EdgeLabelT](metaclass=GraphMeta):
    vertices: VertexView
    edges: BaseEdgeView
    reinit: Callable[[], Self]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseGraph) and self.vertices == other.vertices and self.edges == other.edges

    def clone(self) -> Self:
        result = self.reinit()

        for vertex, label in self.vertices.get_labeled():
            result.vertices[vertex] = label

        for edge, label in self.edges.get_labeled():
            result.edges[edge] = label

        return result

    def induced(self, vertices: Collection[VertT]) -> Self:
        result = self.reinit()

        for vertex, label in self.vertices.get_labeled():
            if vertex in vertices:
                result.vertices[vertex] = label

        for edge, label in self.edges.get_labeled():
            if all(endpoint in vertices for endpoint in edge):
                result.edges[edge] = label

        return result
