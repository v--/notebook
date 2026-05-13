from collections.abc import Collection, Iterator
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from notebook.math.graphs.graph.payload import GraphPayload, LabeledEdge


class BaseEdgeView[VertT, EdgeT: Collection, VertLabelT, EdgeLabelT]:  # noqa: PLW1641
    payload: GraphPayload[VertT, EdgeT, VertLabelT, EdgeLabelT]

    def __init__(self, payload: GraphPayload[VertT, EdgeT, VertLabelT, EdgeLabelT]) -> None:
        self.payload = payload

    @property
    def default_label(self) -> EdgeLabelT:
        return self.payload.default_edge_label

    def add(self, edge: EdgeT) -> None:
        self.payload.set_edge(edge)

    def remove(self, edge: EdgeT) -> None:
        self.payload.remove_edge(edge)

    def get_labeled(self) -> Collection[LabeledEdge[EdgeT, EdgeLabelT]]:
        return self.payload.get_labeled_edges()

    def __contains__(self, edge: EdgeT) -> bool:
        return self.payload.has_edge(edge)

    def __getitem__(self, edge: EdgeT) -> EdgeLabelT:
        return self.payload.get_edge_label(edge)

    def __setitem__(self, edge: EdgeT, label: EdgeLabelT) -> None:
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
