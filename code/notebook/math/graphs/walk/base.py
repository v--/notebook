import functools
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from typing import Any, Self

from ..exceptions import GraphWalkError


@dataclass(frozen=True)
class GraphWalkSegment[VertT, EdgeT: Collection]:
    edge: EdgeT
    tail: VertT


class BaseGraphWalkMeta[VertT, EdgeT: Collection](type):
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        result = super().__call__(*args, **kwargs)
        result.clone_initial = functools.partial(cls.__call__, *args, **kwargs)
        return result


class BaseGraphWalk[VertT, EdgeT: Collection](metaclass=BaseGraphWalkMeta):
    clone_initial: Callable[[], Self]

    _segments: list[GraphWalkSegment[VertT, EdgeT]]
    _tail: VertT
    _head: VertT

    @property
    def segments(self) -> Sequence[GraphWalkSegment[VertT, EdgeT]]:
        return self._segments

    @property
    def tail(self) -> VertT:
        return self._tail

    @property
    def head(self) -> VertT:
        return self._head

    def __init__(self, head: VertT) -> None:
        self._head = head
        self._tail = head
        self._segments = []

    def is_appendable(self, segment: GraphWalkSegment[VertT, EdgeT]) -> bool:
        return self.tail in segment.edge

    def append(self, segment: GraphWalkSegment[VertT, EdgeT]) -> None:
        if not self.is_appendable(segment):
            raise GraphWalkError(f'Cannot append {segment!r} to the existing path')

        self._segments.append(segment)
        self._tail = segment.tail

    def __add__(self, other: 'BaseGraphWalk[VertT, EdgeT]') -> 'BaseGraphWalk[VertT, EdgeT]':
        if not isinstance(other, BaseGraphWalk):
            return NotImplemented

        if self.tail != other.head:
            return NotImplemented

        result = self.clone_initial()

        for segment in self.segments:
            result.append(segment)

        for segment in other.segments:
            result.append(segment)

        return result

    def __len__(self) -> int:
        return len(self.segments)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseGraphWalk):
            return NotImplemented

        return self.head == other.head and self.segments == other.segments

    def iter_vertices(self) -> Iterable[VertT]:
        yield self.head

        for segment in self.segments:
            yield segment.tail
