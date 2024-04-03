from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar


VertT = TypeVar('VertT')
AttrVertT = TypeVar('AttrVertT')
AttrArcT = TypeVar('AttrArcT')


@dataclass
class VertexView(Generic[VertT, AttrVertT, AttrArcT]):
    graph: 'DirectedGraph[VertT, AttrVertT, AttrArcT]'

    def __contains__(self, key: VertT) -> bool:
        return key in self.graph.vertex_dict

    def __getitem__(self, key: VertT) -> AttrVertT | None:
        assert key in self
        return self.graph.vertex_dict[key]

    def __setitem__(self, key: VertT, value: AttrVertT | None) -> None:
        if key not in self.graph.arc_dict:
            self.graph.arc_dict[key] = {}

        self.graph.vertex_dict[key] = value

    def add(self, key: VertT) -> None:
        self[key] = None

    def keys(self) -> Iterable[VertT]:
        return self.graph.vertex_dict.keys()

    def values(self) -> Iterable[AttrVertT | None]:
        return self.graph.vertex_dict.values()

    def items(self) -> Iterable[tuple[VertT, AttrVertT | None]]:
        return self.graph.vertex_dict.items()

    def __iter__(self) -> Iterator[tuple[VertT, AttrVertT | None]]:
        return iter(self.items())


@dataclass
class ArcView(Generic[VertT, AttrVertT, AttrArcT]):
    graph: 'DirectedGraph[VertT, AttrVertT, AttrArcT]'

    def __contains__(self, key: tuple[VertT, VertT]) -> bool:
        assert isinstance(key, tuple)
        assert len(key) == 2
        src, dest = key
        return src in self.graph.vertices and dest in self.graph.arc_dict[src]

    def __getitem__(self, key: tuple[VertT, VertT]) -> AttrArcT | None:
        assert key in self
        src, dest = key
        return self.graph.arc_dict[src][dest]

    def __setitem__(self, key: tuple[VertT, VertT], value: AttrArcT | None) -> None:
        assert isinstance(key, tuple)
        assert len(key) == 2
        src, dest = key

        if src not in self.graph.vertices:
            self.graph.vertices.add(src)

        if dest not in self.graph.vertices:
            self.graph.vertices.add(dest)

        self.graph.arc_dict[src][dest] = value

    def add(self, src: VertT, dest: VertT) -> None:
        self[src, dest] = None

    def __iter__(self) -> Iterator[tuple[VertT, VertT, AttrArcT | None]]:
        for src, dest_map in self.graph.arc_dict.items():
            for dest, label in dest_map.items():
                yield src, dest, label


class DirectedGraph(Generic[VertT, AttrVertT, AttrArcT]):
    vertex_dict: dict[VertT, AttrVertT | None]
    vertices: VertexView[VertT, AttrVertT, AttrArcT]
    arc_dict: dict[VertT, dict[VertT, AttrArcT | None]]
    arcs: ArcView[VertT, AttrVertT, AttrArcT]

    def __init__(
        self,
        vertices: dict[VertT, AttrVertT | None] | None = None,
        arcs: dict[VertT, dict[VertT, AttrArcT | None]] | None = None
    ) -> None:
        self.vertex_dict = vertices or {}
        self.arc_dict = arcs or {}
        self.vertices = VertexView(self)
        self.arcs = ArcView(self)

    def get_in_arcs(self, dest: VertT) -> Iterable[tuple[VertT, AttrArcT | None]]:
        assert dest in self.vertices
        return (
            (in_vert, attr)
            for in_vert, arc in self.arc_dict.items()
            for out_vert, attr in arc.items()
            if out_vert == dest
        )

    def get_out_arcs(self, src: VertT) -> Iterable[tuple[VertT, AttrArcT | None]]:
        assert src in self.vertices
        return self.arc_dict[src].items()

    def __str__(self) -> str:
        return '\n'.join(f'{src} -{label}-> {dest}' for src, dest, label in self.arcs)


def union(*graphs: DirectedGraph[VertT, AttrVertT, AttrArcT]) -> DirectedGraph[VertT, AttrVertT, AttrArcT]:
    result: DirectedGraph[VertT, AttrVertT, AttrArcT] = DirectedGraph()

    for graph in graphs:
        for vert, vert_label in graph.vertices:
            if vert in result.vertices:
                assert result.vertices[vert] == vert_label
            else:
                result.vertices[vert] = vert_label

    for graph in graphs:
        for src, dest, arc_label in graph.arcs:
            if (src, dest) in result.arcs:
                assert result.arcs[src, dest] == arc_label
            else:
                result.arcs[src, dest] = arc_label

    return result
