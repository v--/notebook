from collections.abc import Collection
from typing import TYPE_CHECKING

from notebook.support.coderefs import collector
from notebook.support.collections import SequentialSet


if TYPE_CHECKING:
    from .base import BaseGraphWalk
    from .directed import DirectedWalk


def are_closed[VertT, EdgeT: Collection](walk: BaseGraphWalk[VertT, EdgeT]) -> bool:
    return walk.head == walk.tail


def is_cycle[VertT, EdgeT: Collection](walk: BaseGraphWalk[VertT, EdgeT]) -> bool:
    return (
        len(walk) > 0 and
        are_closed(walk) and
        len(SequentialSet(walk.iter_vertices())) == len(walk) and
        not (len(walk.segments) == 2 and walk.segments[0].edge == walk.segments[1].edge)
    )


@collector.ref('alg:cycle_removal')
def remove_cycles[VertT](walk: DirectedWalk[VertT]) -> DirectedWalk[VertT]:
    if len(walk.segments) == 0:
        return walk

    result = walk.clone_initial()

    current_vertex = walk.head
    last_compatible_index = 0

    while last_compatible_index + 1 < len(walk.segments):
        for i, segment in enumerate(walk.segments):
            if segment.edge.src == current_vertex:
                last_compatible_index = i

        segment = walk.segments[last_compatible_index]
        result.append(segment)
        current_vertex = segment.tail

    return result
