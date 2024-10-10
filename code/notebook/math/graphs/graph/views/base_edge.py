from collections.abc import Collection, Iterator

from ..payload import GraphPayload, LabeledEdge


class BaseEdgeView[VertT, EdgeT: Collection, VertLabelT, EdgeSymbolT]:
    payload: GraphPayload[VertT, EdgeT, VertLabelT, EdgeSymbolT]

    def __init__(self, payload: GraphPayload[VertT, EdgeT, VertLabelT, EdgeSymbolT]) -> None:
        self.payload = payload

    @property
    def default_label(self) -> EdgeSymbolT:
        return self.payload.default_edge_label

    def add(self, edge: EdgeT) -> None:
        self.payload.set_edge(edge)

    def remove(self, edge: EdgeT) -> None:
        self.payload.remove_edge(edge)

    def get_labeled(self) -> Collection[LabeledEdge[EdgeT, EdgeSymbolT]]:
        return self.payload.get_labeled_edges()

    def __contains__(self, edge: EdgeT) -> bool:
        return self.payload.has_edge(edge)

    def __getitem__(self, edge: EdgeT) -> EdgeSymbolT:
        return self.payload.get_edge_label(edge)

    def __setitem__(self, edge: EdgeT, label: EdgeSymbolT) -> None:
        self.payload.set_edge(edge, label)

    def __delitem__(self, edge: EdgeT) -> None:
        self.payload.remove_edge(edge)

    def __len__(self) -> int:
        return self.payload.get_edge_count()

    def __iter__(self) -> Iterator[EdgeT]:
        return iter(self.payload.get_edges())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEdgeView):
            return NotImplemented

        return self.payload.get_labeled_edges() == other.payload.get_labeled_edges()
