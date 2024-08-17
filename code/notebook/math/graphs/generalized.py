from collections.abc import Collection, Hashable, Iterator
from typing import Generic, TypeVar, cast, overload

from .exceptions import GraphError


class ArcCardinalityError(GraphError):
    pass


class MissingVertexError(GraphError):
    pass


class MissingArcError(GraphError):
    pass


VertT = TypeVar('VertT', bound=Hashable)

# In our "generalized graphs", we have "hyperarcs" (vertex iterables) that can be directed arcs or undirected edges.
# GeneralizedArcT should ideally be parameterized on VertT, however mypy doesn't support this
# See https://github.com/python/typing/issues/548
GeneralizedArcT = TypeVar('GeneralizedArcT', bound=Collection[Hashable])

VertLabelT = TypeVar('VertLabelT')
ArcLabelT = TypeVar('ArcLabelT')


class VertexView(Generic[VertT, GeneralizedArcT, VertLabelT, ArcLabelT]):
    _vertex_map: dict[VertT, VertLabelT]
    _arc_map: dict[GeneralizedArcT, ArcLabelT]

    def __init__(self, vertex_map: dict[VertT, VertLabelT], arc_map: dict[GeneralizedArcT, ArcLabelT]) -> None:
        self._vertex_map = vertex_map
        self._arc_map = arc_map

    def __contains__(self, vertex: object) -> bool:
        return vertex in self._vertex_map

    @overload
    def add(self: 'VertexView[VertT, GeneralizedArcT, None, ArcLabelT]', vertex: VertT) -> None: ...
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


class GeneralizedArcView(Generic[VertT, GeneralizedArcT, VertLabelT, ArcLabelT]):
    _vertex_map: dict[VertT, VertLabelT]
    _arc_map: dict[GeneralizedArcT, ArcLabelT]

    def __init__(self, vertex_map: dict[VertT, VertLabelT], arc_map: dict[GeneralizedArcT, ArcLabelT]) -> None:
        self._vertex_map = vertex_map
        self._arc_map = arc_map

    @overload
    def add(self: 'GeneralizedArcView[VertT, GeneralizedArcT, VertLabelT, None]', arc: GeneralizedArcT) -> None: ...
    @overload
    def add(self, arc: GeneralizedArcT, label: ArcLabelT) -> None: ...
    def add(self, arc: GeneralizedArcT, label: ArcLabelT | None = None) -> None:
        if len(arc) == 0:
            raise ArcCardinalityError(f'Too few endpoints in {arc!r}')

        if len(arc) > 2:
            raise ArcCardinalityError(f'Too many endpoints in {arc!r}')

        for endpoint in arc:
            if endpoint not in self._vertex_map:
                # We cannot determine whether VertLabelT is None, so we simply hope this won't get abused
                self._vertex_map[cast(VertT, endpoint)] = cast(VertLabelT, None)

        self._arc_map[arc] = cast(ArcLabelT, label)

    def remove(self, arc: GeneralizedArcT) -> None:
        del self._arc_map[arc]

    def get_label(self, arc: GeneralizedArcT) -> ArcLabelT:
        if arc not in self:
            raise MissingArcError(f'No such arc {arc!r}')

        return self._arc_map[arc]

    def __len__(self) -> int:
        return len(self._arc_map)

    def __iter__(self) -> Iterator[GeneralizedArcT]:
        return iter(self._arc_map)


class GeneralizedDirectedGraph(Generic[VertT, GeneralizedArcT, VertLabelT, ArcLabelT]):
    vertices: VertexView[VertT, GeneralizedArcT, VertLabelT, ArcLabelT]
    arcs: GeneralizedArcView[VertT, GeneralizedArcT, VertLabelT, ArcLabelT]

    @classmethod
    def create_vertex_view(cls, vertex_map: dict[VertT, VertLabelT], arc_map: dict[GeneralizedArcT, ArcLabelT]) -> VertexView:
        return VertexView(vertex_map, arc_map)

    @classmethod
    def create_arc_view(cls, vertex_map: dict[VertT, VertLabelT], arc_map: dict[GeneralizedArcT, ArcLabelT]) -> GeneralizedArcView:
        return GeneralizedArcView(vertex_map, arc_map)

    def __init__(self) -> None:
        vertex_map: dict[VertT, VertLabelT] = {}
        arc_map: dict[GeneralizedArcT, ArcLabelT] = {}
        self.vertices = self.create_vertex_view(vertex_map, arc_map)
        self.arcs = self.create_arc_view(vertex_map, arc_map)


class GeneralizedUndirectedGraph(Generic[VertT, GeneralizedArcT, VertLabelT, ArcLabelT]):
    vertices: VertexView[VertT, GeneralizedArcT, VertLabelT, ArcLabelT]
    arcs: GeneralizedArcView[VertT, GeneralizedArcT, VertLabelT, ArcLabelT]

    @classmethod
    def create_vertex_view(cls, vertex_map: dict[VertT, VertLabelT], edge_map: dict[GeneralizedArcT, ArcLabelT]) -> VertexView[VertT, GeneralizedArcT, VertLabelT, ArcLabelT]:
        return VertexView(vertex_map, edge_map)

    @classmethod
    def create_edge_view(cls, vertex_map: dict[VertT, VertLabelT], edge_map: dict[GeneralizedArcT, ArcLabelT]) -> GeneralizedArcView[VertT, GeneralizedArcT, VertLabelT, ArcLabelT]:
        return GeneralizedArcView(vertex_map, edge_map)

    def __init__(self) -> None:
        vertex_map: dict[VertT, VertLabelT] = {}
        edge_map: dict[GeneralizedArcT, ArcLabelT] = {}
        self.vertices = self.create_vertex_view(vertex_map, edge_map)
        self.edges = self.create_edge_view(vertex_map, edge_map)
