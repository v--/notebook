from typing import cast, overload, override

from .generalized import (
    ArcLabelT,
    GeneralizedArcView,
    GeneralizedDirectedGraph,
    GeneralizedUndirectedGraph,
    VertLabelT,
    VertT,
)


class ArcView(GeneralizedArcView[VertT, tuple[VertT, VertT], VertLabelT, ArcLabelT]):
    def _add_arc(self, arc: tuple[VertT, VertT], label: ArcLabelT | None = None) -> None:
        super().add(arc, cast(ArcLabelT, label))

    def _add_src_dest(self, src: VertT, dest: VertT, label: ArcLabelT | None = None) -> None:
        self._add_arc((src, dest), label)

    @overload
    def add(self: 'ArcView[VertT, VertLabelT, None]', arc: tuple[VertT, VertT]) -> None: ...
    @overload
    def add(self: 'ArcView[VertT, VertLabelT, None]', src: VertT, dest: VertT) -> None: ...
    @overload
    def add(self, arc: tuple[VertT, VertT], label: ArcLabelT) -> None: ...
    @overload
    def add(self, src: VertT, dest: VertT, label: ArcLabelT) -> None: ...
    def add(self, *args, **kwargs) -> None:
        if 'arc' in kwargs or (len(args) > 0 and isinstance(args[0], tuple)):
            self._add_arc(*args, **kwargs)
        else:
            self._add_src_dest(*args, **kwargs)

    @overload
    def remove(self, a: tuple[VertT, VertT]) -> None: ...
    @overload
    def remove(self, a: VertT, b: VertT) -> None: ...
    @override
    def remove(self, a: tuple[VertT, VertT] | VertT, b: VertT | None = None) -> None:
        if b is None:
            a_ = cast(tuple[VertT, VertT], a)
            super().remove(a_)
        else:
            a__ = cast(VertT, a)
            super().remove((a__, b))


class DirectedGraph(GeneralizedDirectedGraph[VertT, tuple[VertT, VertT], VertLabelT, ArcLabelT]):
    arcs: ArcView[VertT, VertLabelT, ArcLabelT]

    @override
    @classmethod
    def create_arc_view(cls, vertex_map: dict[VertT, VertLabelT], arc_map: dict[tuple[VertT, VertT], ArcLabelT]) -> ArcView[VertT, VertLabelT, ArcLabelT]:
        return ArcView(vertex_map, arc_map)


class EdgeView(GeneralizedArcView[VertT, frozenset[VertT], VertLabelT, ArcLabelT]):
    def _add_edge(self, edge: frozenset[VertT], label: ArcLabelT | None = None) -> None:
        super().add(edge, cast(ArcLabelT, label))

    def _add_src_dest(self, src: VertT, dest: VertT, label: ArcLabelT | None = None) -> None:
        self._add_edge(frozenset([src, dest]), label)

    @overload
    def add(self: 'EdgeView[VertT, VertLabelT, None]', edge: frozenset[VertT]) -> None: ...
    @overload
    def add(self: 'EdgeView[VertT, VertLabelT, None]', src: VertT, dest: VertT) -> None: ...
    @overload
    def add(self, edge: frozenset[VertT], label: ArcLabelT) -> None: ...
    @overload
    def add(self, src: VertT, dest: VertT, label: ArcLabelT) -> None: ...
    def add(self, *args, **kwargs) -> None:
        if 'edge' in kwargs or (len(args) > 0 and isinstance(args[0], frozenset)):
            self._add_edge(*args, **kwargs)
        else:
            self._add_src_dest(*args, **kwargs)

    @overload
    def remove(self, a: frozenset[VertT]) -> None: ...
    @overload
    def remove(self, a: VertT, b: VertT) -> None: ...
    @override
    def remove(self, a: frozenset[VertT] | VertT, b: VertT | None = None) -> None:
        if b is None:
            a_ = cast(frozenset[VertT], a)
            super().remove(a_)
        else:
            a__ = cast(VertT, a)
            super().remove(frozenset([a__, b]))


class UndirectedGraph(GeneralizedUndirectedGraph[VertT, frozenset[VertT], VertLabelT, ArcLabelT]):
    edges: EdgeView[VertT, VertLabelT, ArcLabelT]

    @override
    @classmethod
    def create_edge_view(cls, vertex_map: dict[VertT, VertLabelT], edge_map: dict[frozenset[VertT], ArcLabelT]) -> EdgeView[VertT, VertLabelT, ArcLabelT]:
        return EdgeView(vertex_map, edge_map)
