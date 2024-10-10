from collections.abc import Collection, Iterator

from ..payload import GraphPayload, LabeledVertex


class VertexView[VertT, EdgeT: Collection, VertLabelT, EdgeSymbolT]:
    payload: GraphPayload[VertT, EdgeT, VertLabelT, EdgeSymbolT]

    def __init__(self, payload: GraphPayload[VertT, EdgeT, VertLabelT, EdgeSymbolT]) -> None:
        self.payload = payload

    @property
    def default_label(self) -> VertLabelT:
        return self.payload.default_vertex_label

    def add(self, vertex: VertT) -> None:
        self.payload.set_vertex(vertex)

    def remove(self, vertex: VertT) -> None:
        self.payload.remove_vertex(vertex)

    def get_labeled(self) -> Collection[LabeledVertex[VertT, VertLabelT]]:
        return self.payload.get_labeled_vertices()

    def __contains__(self, vertex: VertT) -> bool:
        return self.payload.has_vertex(vertex)

    def __getitem__(self, vertex: VertT) -> VertLabelT:
        return self.payload.get_vertex_label(vertex)

    def __setitem__(self, vertex: VertT, label: VertLabelT) -> None:
        self.payload.set_vertex(vertex, label)

    def __delitem__(self, vertex: VertT) -> None:
        self.payload.remove_vertex(vertex)

    def __len__(self) -> int:
        return self.payload.get_vertex_count()

    def __iter__(self) -> Iterator[VertT]:
        return iter(self.payload.get_vertices())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VertexView):
            return NotImplemented

        return self.payload.get_labeled_vertices() == other.payload.get_labeled_vertices()
