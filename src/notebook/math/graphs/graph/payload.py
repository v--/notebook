from collections.abc import Collection, MutableMapping
from itertools import starmap
from typing import NamedTuple, cast, overload

from notebook.math.graphs.exceptions import MissingEdgeError, MissingVertexError
from notebook.support.collections import SequentialMapping


class LabeledVertex[VertT, VertLabelT](NamedTuple):
    vertex: VertT
    label: VertLabelT


class LabeledEdge[EdgeT: Collection, EdgeLabelT](NamedTuple):
    vertex: EdgeT
    label: EdgeLabelT


class GraphPayload[VertT, EdgeT: Collection, VertLabelT, EdgeLabelT]:
    _vertex_map: MutableMapping[VertT, VertLabelT]
    _edge_map: MutableMapping[EdgeT, EdgeLabelT]
    default_vertex_label: VertLabelT
    default_edge_label: EdgeLabelT

    @overload
    def __init__(self, *, default_vertex_label: VertLabelT, default_edge_label: EdgeLabelT) -> None: ...
    @overload
    def __init__(self: GraphPayload[VertT, EdgeT, VertLabelT, None], *, default_vertex_label: VertLabelT) -> None: ...
    @overload
    def __init__(self: GraphPayload[VertT, EdgeT, None, EdgeLabelT], *, default_edge_label: EdgeLabelT) -> None: ...
    @overload
    def __init__(self: GraphPayload[VertT, EdgeT, None, None]) -> None: ...
    def __init__(self, *, default_vertex_label: VertLabelT | None = None, default_edge_label: EdgeLabelT | None = None) -> None:
        self._vertex_map = SequentialMapping()
        self._edge_map = SequentialMapping()
        self.default_vertex_label = cast('VertLabelT', default_vertex_label)
        self.default_edge_label = cast('EdgeLabelT', default_edge_label)

    def has_vertex(self, vertex: VertT) -> bool:
        return vertex in self._vertex_map

    def set_vertex(self, vertex: VertT, label: VertLabelT | None = None) -> None:
        self._vertex_map[vertex] = label if label is not None else self.default_vertex_label

    def remove_vertex(self, vertex: VertT) -> None:
        try:
            del self._vertex_map[vertex]
        except KeyError:
            raise MissingVertexError(f'The vertex {vertex!r} is in not in the graph') from None

        for edge in list(self._edge_map):
            if vertex in edge:
                del self._edge_map[edge]

    def get_vertex_label(self, vertex: VertT) -> VertLabelT:
        try:
            return self._vertex_map[vertex]
        except KeyError:
            raise MissingVertexError(f'The vertex {vertex!r} is in not in the graph') from None

    def get_vertices(self) -> Collection[VertT]:
        return self._vertex_map.keys()

    def get_labeled_vertices(self) -> Collection[LabeledVertex[VertT, VertLabelT]]:
        return list(starmap(LabeledVertex, self._vertex_map.items()))

    def get_vertex_count(self) -> int:
        return len(self._vertex_map)

    def has_edge(self, edge: EdgeT) -> bool:
        return edge in self._edge_map

    def set_edge(self, edge: EdgeT, label: EdgeLabelT | None = None) -> None:
        for vertex in edge:
            if vertex not in self._vertex_map:
                self._vertex_map[vertex] = self.default_vertex_label

        self._edge_map[edge] = label if label is not None else self.default_edge_label

    def remove_edge(self, edge: EdgeT) -> None:
        try:
            del self._edge_map[edge]
        except KeyError:
            raise MissingEdgeError(f'The edge {edge!r} is in not in the graph') from None

    def get_edge_label(self, edge: EdgeT) -> EdgeLabelT:
        try:
            return self._edge_map[edge]
        except KeyError:
            raise MissingVertexError(f'The vertex {edge!r} is in not in the graph') from None

    def get_edges(self) -> Collection[EdgeT]:
        return self._edge_map.keys()

    def get_labeled_edges(self) -> Collection[LabeledEdge[EdgeT, EdgeLabelT]]:
        return list(starmap(LabeledEdge, self._edge_map.items()))

    def get_edge_count(self) -> int:
        return len(self._edge_map)
