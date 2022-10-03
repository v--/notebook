from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar


TVert = TypeVar('TVert')
TAttrVert = TypeVar('TAttrVert')
TAttrArc = TypeVar('TAttrArc')


@dataclass
class VertexView(Generic[TVert, TAttrVert]):
    graph: DirectedGraph

    def __contains__(self, key: TVert):
        return key in self.graph._vertices

    def __getitem__(self, key: TVert) -> TAttrVert | None:
        assert key in self
        return self.graph._vertices[key]

    def __setitem__(self, key: TVert, value: TAttrVert | None):
        if key not in self.graph._arcs:
            self.graph._arcs[key] = {}

        self.graph._vertices[key] = value

    def add(self, key: TVert):
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
class ArcView(Generic[TVert, TAttrArc]):
    graph: DirectedGraph

    def __contains__(self, key: tuple[TVert, TVert]):
        assert isinstance(key, tuple) and len(key) == 2
        src, dest = key
        return src in self.graph.vertices and dest in self.graph._arcs[src]

    def __getitem__(self, key: tuple[TVert, TVert]):
        assert key in self
        src, dest = key
        return self.graph._arcs[src][dest]

    def __setitem__(self, key: tuple[TVert, TVert], value: TAttrArc | None):
        assert isinstance(key, tuple) and len(key) == 2
        src, dest = key

        if src not in self.graph.vertices:
            self.graph.vertices.add(src)

        if dest not in self.graph.vertices:
            self.graph.vertices.add(dest)

        self.graph._arcs[src][dest] = value

    def add(self, src: TVert, dest: TVert):
        self[src, dest] = None

    def __iter__(self):
        for src, dest_map in self.graph._arcs.items():
            for dest, label in dest_map.items():
                yield src, dest, label


class DirectedGraph(Generic[TVert, TAttrVert, TAttrArc]):
    _vertices: dict[TVert, TAttrVert]
    vertices: VertexView
    _arcs: dict[TVert, dict[TVert, TAttrArc]]
    arcs: ArcView

    def __init__(
        self,
        vertices: dict[TVert, TAttrVert] | None = None,
        arcs: dict[TVert, dict[TVert, TAttrArc]] | None = None
    ):
        self._vertices = vertices or {}
        self._arcs = arcs or {}
        self.vertices = VertexView(self)
        self.arcs = ArcView(self)

    def get_in_arcs(self, dest: TVert):
        assert dest in self.vertices
        return (
            (in_vert, attr)
            for in_vert, arc in self._arcs.items()
            for out_vert, attr in arc.items()
            if out_vert == dest
        )

    def get_out_arcs(self, src: TVert):
        assert src in self.vertices
        return self._arcs[src].items()

    def __str__(self):
        return '\n'.join(f'{src} -{label}-> {dest}' for src, dest, label in self.arcs)


def union(*graphs: DirectedGraph[TVert, TAttrVert, TAttrArc]) -> DirectedGraph[TVert, TAttrVert, TAttrArc]:
    result: DirectedGraph[TVert, TAttrVert, TAttrArc] = DirectedGraph()

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
