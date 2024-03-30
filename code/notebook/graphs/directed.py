from dataclasses import dataclass
from typing import Generic, TypeVar


VertT = TypeVar('VertT')
AttrVertT = TypeVar('AttrVertT')
AttrArcT = TypeVar('AttrArcT')


@dataclass
class VertexView(Generic[VertT, AttrVertT]):
    graph: 'DirectedGraph'

    def __contains__(self, key: VertT):
        return key in self.graph._vertices

    def __getitem__(self, key: VertT) -> AttrVertT | None:
        assert key in self
        return self.graph._vertices[key]

    def __setitem__(self, key: VertT, value: AttrVertT | None):
        if key not in self.graph._arcs:
            self.graph._arcs[key] = {}

        self.graph._vertices[key] = value

    def add(self, key: VertT):
        self[key] = None

    def keys(self):
        return self.graph._vertices.keys()

    def values(self):
        return self.graph._vertices.values()

    def items(self):
        return self.graph._vertices.items()

    def __iter__(self):
        return iter(self.items())


@dataclass
class ArcView(Generic[VertT, AttrArcT]):
    graph: 'DirectedGraph'

    def __contains__(self, key: tuple[VertT, VertT]):
        assert isinstance(key, tuple) and len(key) == 2
        src, dest = key
        return src in self.graph.vertices and dest in self.graph._arcs[src]

    def __getitem__(self, key: tuple[VertT, VertT]):
        assert key in self
        src, dest = key
        return self.graph._arcs[src][dest]

    def __setitem__(self, key: tuple[VertT, VertT], value: AttrArcT | None):
        assert isinstance(key, tuple) and len(key) == 2
        src, dest = key

        if src not in self.graph.vertices:
            self.graph.vertices.add(src)

        if dest not in self.graph.vertices:
            self.graph.vertices.add(dest)

        self.graph._arcs[src][dest] = value

    def add(self, src: VertT, dest: VertT):
        self[src, dest] = None

    def __iter__(self):
        for src, dest_map in self.graph._arcs.items():
            for dest, label in dest_map.items():
                yield src, dest, label


class DirectedGraph(Generic[VertT, AttrVertT, AttrArcT]):
    _vertices: dict[VertT, AttrVertT]
    vertices: VertexView
    _arcs: dict[VertT, dict[VertT, AttrArcT]]
    arcs: ArcView

    def __init__(
        self,
        vertices: dict[VertT, AttrVertT] | None = None,
        arcs: dict[VertT, dict[VertT, AttrArcT]] | None = None
    ):
        self._vertices = vertices or {}
        self._arcs = arcs or {}
        self.vertices = VertexView(self)
        self.arcs = ArcView(self)

    def get_in_arcs(self, dest: VertT):
        assert dest in self.vertices
        return (
            (in_vert, attr)
            for in_vert, arc in self._arcs.items()
            for out_vert, attr in arc.items()
            if out_vert == dest
        )

    def get_out_arcs(self, src: VertT):
        assert src in self.vertices
        return self._arcs[src].items()

    def __str__(self):
        return '\n'.join(f'{src} -{label}-> {dest}' for src, dest, label in self.arcs)


def union(*graphs: DirectedGraph[VertT, AttrVertT, AttrArcT]) -> DirectedGraph[VertT, AttrVertT, AttrArcT]:
    result: DirectedGraph[VertT, AttrVertT, AttrArcT] = DirectedGraph()

    for graph in graphs:
        for vert, label in graph.vertices:
            if vert in result.vertices:
                assert result.vertices[vert] == label
            else:
                result.vertices[vert] = label

    for graph in graphs:
        for src, dest, label in graph.arcs:
            if (src, dest) in result.arcs:
                assert result.arcs[src, dest] == label
            else:
                result.arcs[src, dest] = label

    return result
