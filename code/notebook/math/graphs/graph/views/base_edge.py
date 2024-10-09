from collections.abc import Collection, Iterator

from ..payload import GraphPayload, LabeledEdge


class BaseEdgeView[VertT, EdgeT: Collection, VertLabelT, EdgeLabelT]:
    payload: GraphPayload[VertT, EdgeT, VertLabelT, EdgeLabelT]

    def __init__(self, payload: GraphPayload) -> None:
        self.payload = payload

    def add(self: 'BaseEdgeView[VertT, EdgeT, VertLabelT, None]', edge: EdgeT) -> None:
        self.payload.add_edge(edge)  # type: ignore[call-overload]

    def remove(self, edge: EdgeT) -> None:
        self.payload.remove_edge(edge)

    def get_labeled(self) -> Collection[LabeledEdge[EdgeT, EdgeLabelT]]:
        return self.payload.get_labeled_edges()

    def __contains__(self, edge: EdgeT) -> bool:
        return self.payload.has_edge(edge)

    def __getitem__(self, edge: EdgeT) -> EdgeLabelT:
        return self.payload.get_edge_label(edge)

    def __setitem__(self, edge: EdgeT, label: EdgeLabelT) -> None:
        self.payload.add_edge(edge, label)

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
