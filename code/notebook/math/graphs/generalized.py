from collections.abc import Collection, Hashable, Iterator
from collections.abc import Set as AbstractSet
from typing import Self, cast, overload

from .exceptions import GraphError


BaseVertType = Hashable


class ArcCardinalityError(GraphError):
    pass


class MissingVertexError(GraphError):
    pass


class MissingArcError(GraphError):
    pass


class VertexView[VertT: BaseVertType, ArcT: Collection[BaseVertType], VertLabelT, ArcLabelT]:
    _vertex_map: dict[VertT, VertLabelT]
    _arc_map: dict[ArcT, ArcLabelT]

    def __init__(self, vertex_map: dict[VertT, VertLabelT], arc_map: dict[ArcT, ArcLabelT]) -> None:
        self._vertex_map = vertex_map
        self._arc_map = arc_map

    def __contains__(self, vertex: object) -> bool:
        return vertex in self._vertex_map

    @overload
    def add(self: 'VertexView[VertT, ArcT, None, ArcLabelT]', vertex: VertT) -> None: ...
    @overload
    def add(self, vertex: VertT, label: VertLabelT) -> None: ...
    def add(self, vertex: VertT, label: VertLabelT | None = None) -> None:
        self._vertex_map[vertex] = cast(VertLabelT, label)

    def remove(self, vertex: VertT) -> None:
        del self._vertex_map[vertex]

        for arc in list(self._arc_map):
            for endpoint in arc:
                if endpoint == vertex:
                    del self._arc_map[arc]

    def get_label(self, vertex: VertT) -> VertLabelT:
        if vertex not in self:
            raise MissingArcError('No such vertex {vertex!r}')

        return self._vertex_map[vertex]

    def __len__(self) -> int:
        return len(self._vertex_map)

    def __iter__(self) -> Iterator[VertT]:
        return iter(self._vertex_map)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VertexView):
            return NotImplemented

        return self._vertex_map == other._vertex_map


class GeneralizedArcView[VertT: BaseVertType, ArcT: Collection[BaseVertType], VertLabelT, ArcLabelT]:
    _vertex_map: dict[VertT, VertLabelT]
    _arc_map: dict[ArcT, ArcLabelT]

    def __init__(self, vertex_map: dict[VertT, VertLabelT], arc_map: dict[ArcT, ArcLabelT]) -> None:
        self._vertex_map = vertex_map
        self._arc_map = arc_map

    @overload
    def add(self: 'GeneralizedArcView[VertT, ArcT, VertLabelT, None]', arc: ArcT) -> None: ...
    @overload
    def add(self, arc: ArcT, label: ArcLabelT) -> None: ...
    def add(self, arc: ArcT, label: ArcLabelT | None = None) -> None:
        if len(arc) == 0:
            raise ArcCardinalityError(f'Too few endpoints in {arc!r}')

        if len(arc) > 2:
            raise ArcCardinalityError(f'Too many endpoints in {arc!r}')

        for endpoint in arc:
            if endpoint not in self._vertex_map:
                # We cannot determine whether VertLabelT is None, so we simply hope this won't get abused
                self._vertex_map[cast(VertT, endpoint)] = cast(VertLabelT, None)

        self._arc_map[arc] = cast(ArcLabelT, label)

    def remove(self, arc: ArcT) -> None:
        del self._arc_map[arc]

    def get_label(self, arc: ArcT) -> ArcLabelT:
        if arc not in self:
            raise MissingArcError(f'No such arc {arc!r}')

        return self._arc_map[arc]

    def __len__(self) -> int:
        return len(self._arc_map)

    def __iter__(self) -> Iterator[ArcT]:
        return iter(self._arc_map)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GeneralizedArcView):
            return NotImplemented

        return self._arc_map == other._arc_map


class GeneralizedDirectedGraph[VertT: BaseVertType, ArcT: Collection[BaseVertType], VertLabelT, ArcLabelT]:
    vertices: VertexView[VertT, ArcT, VertLabelT, ArcLabelT]
    arcs: GeneralizedArcView[VertT, ArcT, VertLabelT, ArcLabelT]

    @classmethod
    def create_vertex_view(cls, vertex_map: dict[VertT, VertLabelT], arc_map: dict[ArcT, ArcLabelT]) -> VertexView:
        return VertexView(vertex_map, arc_map)

    @classmethod
    def create_arc_view(cls, vertex_map: dict[VertT, VertLabelT], arc_map: dict[ArcT, ArcLabelT]) -> GeneralizedArcView:
        return GeneralizedArcView(vertex_map, arc_map)

    def __init__(self) -> None:
        vertex_map: dict[VertT, VertLabelT] = {}
        arc_map: dict[ArcT, ArcLabelT] = {}
        self.vertices = self.create_vertex_view(vertex_map, arc_map)
        self.arcs = self.create_arc_view(vertex_map, arc_map)

    def dup(self) -> Self:
        result = type(self)()

        for arc in self.arcs:
            result.arcs.add(arc, self.arcs.get_label(arc))

        return result

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GeneralizedDirectedGraph):
            return NotImplemented

        return self.vertices == other.vertices and self.arcs == other.arcs


class GeneralizedUndirectedGraph[VertT: BaseVertType, ArcT: Collection[BaseVertType], VertLabelT, ArcLabelT]:
    vertices: VertexView[VertT, ArcT, VertLabelT, ArcLabelT]
    arcs: GeneralizedArcView[VertT, ArcT, VertLabelT, ArcLabelT]

    @classmethod
    def create_vertex_view(cls, vertex_map: dict[VertT, VertLabelT], edge_map: dict[ArcT, ArcLabelT]) -> VertexView[VertT, ArcT, VertLabelT, ArcLabelT]:
        return VertexView(vertex_map, edge_map)

    @classmethod
    def create_edge_view(cls, vertex_map: dict[VertT, VertLabelT], edge_map: dict[ArcT, ArcLabelT]) -> GeneralizedArcView[VertT, ArcT, VertLabelT, ArcLabelT]:
        return GeneralizedArcView(vertex_map, edge_map)

    def __init__(self) -> None:
        vertex_map: dict[VertT, VertLabelT] = {}
        edge_map: dict[ArcT, ArcLabelT] = {}
        self.vertices = self.create_vertex_view(vertex_map, edge_map)
        self.edges = self.create_edge_view(vertex_map, edge_map)

    def induced(self, vertices: AbstractSet[VertT] | tuple[VertT, ...]) -> Self:
        result = type(self)()

        for vertex in vertices:
            result.vertices.add(vertex, self.vertices.get_label(vertex))

        for edge in self.edges:
            if all(v in vertices for v in edge):
                result.edges.add(edge, self.edges.get_label(edge))

        return result

    def dup(self) -> Self:
        result = type(self)()

        for edge in self.edges:
            result.edges.add(edge, self.edges.get_label(edge))

        return result

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GeneralizedUndirectedGraph):
            return NotImplemented

        return self.vertices == other.vertices and self.edges == other.edges
