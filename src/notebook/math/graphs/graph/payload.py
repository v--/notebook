from collections.abc import Collection, MutableMapping
from typing import NamedTuple, overload

from ....support.collections.sequential_mapping import SequentialMapping
from ....support.typing import typesup
from ..exceptions import MissingEdgeError, MissingVertexError


class LabeledVertex[VertT, VertLabelT](NamedTuple):
    vertex: VertT
    label: VertLabelT


class LabeledEdge[EdgeT: Collection, EdgeSymbolT](NamedTuple):
    vertex: EdgeT
    label: EdgeSymbolT


class GraphPayload[VertT, EdgeT: Collection, VertLabelT, EdgeSymbolT]:
    _vertex_map: MutableMapping[VertT, VertLabelT]
    _edge_map: MutableMapping[EdgeT, EdgeSymbolT]
    default_vertex_label: VertLabelT
    default_edge_label: EdgeSymbolT

    @overload
    def __init__(self, *, default_vertex_label: VertLabelT, default_edge_label: EdgeSymbolT) -> None: ...
    @overload
    def __init__(self: GraphPayload[VertT, EdgeT, VertLabelT, None], *, default_vertex_label: VertLabelT) -> None: ...
    @overload
    def __init__(self: GraphPayload[VertT, EdgeT, None, EdgeSymbolT], *, default_edge_label: EdgeSymbolT) -> None: ...
    @overload
    def __init__(self: GraphPayload[VertT, EdgeT, None, None]) -> None: ...
    def __init__(self, *, default_vertex_label: VertLabelT | None = None, default_edge_label: EdgeSymbolT | None = None) -> None:
        self._vertex_map = SequentialMapping()
        self._edge_map = SequentialMapping()
        self.default_vertex_label = typesup(default_vertex_label)
        self.default_edge_label = typesup(default_edge_label)

    def has_vertex(self, vertex: VertT) -> bool:
        return vertex in self._vertex_map

    def set_vertex(self, vertex: VertT, label: VertLabelT | None = None) -> None:
        self._vertex_map[vertex] = label if label is not None else self.default_vertex_label

    def remove_vertex(self, vertex: VertT) -> None:
        try:
            del self._vertex_map[vertex]
        except KeyError:
            raise MissingVertexError(f'The vertex {vertex!r} is in not in the graph') from None

        for edge in self._edge_map.keys():
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
        return [LabeledVertex(*t) for t in self._vertex_map.items()]

    def get_vertex_count(self) -> int:
        return len(self._vertex_map)

    def has_edge(self, edge: EdgeT) -> bool:
        return edge in self._edge_map

    def set_edge(self, edge: EdgeT, label: EdgeSymbolT | None = None) -> None:
        for vertex in edge:
            if vertex not in self._vertex_map:
                self._vertex_map[vertex] = self.default_vertex_label

        self._edge_map[edge] = label if label is not None else self.default_edge_label

    def remove_edge(self, edge: EdgeT) -> None:
        try:
            del self._edge_map[edge]
        except KeyError:
            raise MissingEdgeError(f'The edge {edge!r} is in not in the graph') from None

    def get_edge_label(self, edge: EdgeT) -> EdgeSymbolT:
        try:
            return self._edge_map[edge]
        except KeyError:
            raise MissingVertexError(f'The vertex {edge!r} is in not in the graph') from None

    def get_edges(self) -> Collection[EdgeT]:
        return self._edge_map.keys()

    def get_labeled_edges(self) -> Collection[LabeledEdge[EdgeT, EdgeSymbolT]]:
        return [LabeledEdge(*t) for t in self._edge_map.items()]

    def get_edge_count(self) -> int:
        return len(self._edge_map)
