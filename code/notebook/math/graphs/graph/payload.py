from collections.abc import Collection
from typing import NamedTuple, cast, overload

from ....support.sequential_mapping import KeyExistsError, MissingKeyError, SequentialMapping
from ..exceptions import EdgeExistsError, MissingEdgeError, MissingVertexError, VertexExistsError


class LabeledVertex[VertT, VertLabelT](NamedTuple):
    vertex: VertT
    label: VertLabelT


class LabeledEdge[EdgeT: Collection, EdgeLabelT](NamedTuple):
    vertex: EdgeT
    label: EdgeLabelT


class GraphPayload[VertT, EdgeT: Collection, VertLabelT, EdgeLabelT]:
    _vertex_map: SequentialMapping[VertT, VertLabelT]
    _edge_map: SequentialMapping[EdgeT, EdgeLabelT]

    def __init__(self) -> None:
        self._vertex_map = SequentialMapping()
        self._edge_map = SequentialMapping()

    def has_vertex(self, vertex: VertT) -> bool:
        return vertex in self._vertex_map

    @overload
    def add_vertex(self: 'GraphPayload[VertT, EdgeT, None, EdgeLabelT]', vertex: VertT) -> None: ...
    @overload
    def add_vertex(self, vertex: VertT, label: VertLabelT) -> None: ...
    def add_vertex(self, vertex: VertT, label: VertLabelT | None = None) -> None:
        try:
            self._vertex_map.set(vertex, cast(VertLabelT, label), exists_ok=False)
        except KeyExistsError:
            raise VertexExistsError(f'The vertex {vertex!r} is already in the graph') from None

    def remove_vertex(self, vertex: VertT, *, remove_edges: bool = False) -> None:
        try:
            del self._vertex_map[vertex]
        except MissingKeyError:
            raise MissingVertexError(f'The vertex {vertex!r} is in not in the graph') from None

        for edge in self._edge_map.keys():
            if vertex in edge:
                if remove_edges:
                    del self._edge_map[edge]
                else:
                    raise EdgeExistsError(f'Cannot delete vertex {vertex!r} while {edge!r} is in the graph') from None

    def get_vertex_label(self, vertex: VertT) -> VertLabelT:
        try:
            return self._vertex_map[vertex]
        except MissingKeyError:
            raise MissingVertexError(f'The vertex {vertex!r} is in not in the graph') from None

    def get_vertices(self) -> Collection[VertT]:
        return self._vertex_map.keys()

    def get_labeled_vertices(self) -> Collection[LabeledVertex[VertT, VertLabelT]]:
        return [LabeledVertex(*t) for t in self._vertex_map.items()]

    def get_vertex_count(self) -> int:
        return len(self._vertex_map)

    def has_edge(self, edge: EdgeT) -> bool:
        return edge in self._edge_map

    @overload
    def add_edge(self: 'GraphPayload[VertT, EdgeT, VertLabelT, None]', edge: EdgeT) -> None: ...
    @overload
    def add_edge(self, edge: EdgeT, label: EdgeLabelT) -> None: ...
    def add_edge(self, edge: EdgeT, label: EdgeLabelT | None = None) -> None:
        for vertex in edge:
            if vertex not in self._vertex_map:
                raise MissingVertexError(f'The endpoint {vertex!r} of {edge!r} in not in the graph')

        try:
            self._edge_map.set(edge, cast(EdgeLabelT, label), exists_ok=False)
        except KeyExistsError:
            raise EdgeExistsError(f'The edge {edge!r} is already in the graph') from None

    def remove_edge(self, edge: EdgeT) -> None:
        try:
            del self._edge_map[edge]
        except KeyExistsError:
            raise MissingEdgeError(f'The edge {edge!r} is in not in the graph') from None

    def get_edge_label(self, edge: EdgeT) -> EdgeLabelT:
        try:
            return self._edge_map[edge]
        except MissingKeyError:
            raise MissingVertexError(f'The vertex {edge!r} is in not in the graph') from None

    def get_edges(self) -> Collection[EdgeT]:
        return self._edge_map.keys()

    def get_labeled_edges(self) -> Collection[LabeledEdge[EdgeT, EdgeLabelT]]:
        return [LabeledEdge(*t) for t in self._edge_map.items()]

    def get_edge_count(self) -> int:
        return len(self._edge_map)
