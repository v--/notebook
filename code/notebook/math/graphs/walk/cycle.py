from collections.abc import Collection

from ....support.collections.sequential_set import SequentialSet
from .base import BaseGraphWalk
from .directed import DirectedWalk


def is_closed[VertT, EdgeT: Collection](walk: BaseGraphWalk[VertT, EdgeT]) -> bool:
    return walk.head == walk.tail


def is_cycle[VertT, EdgeT: Collection](walk: BaseGraphWalk[VertT, EdgeT]) -> bool:
    return (
        len(walk) > 0 and \
        is_closed(walk) and \
        len(SequentialSet(walk.iter_vertices())) == len(walk) and \
        not (len(walk.segments) == 2 and walk.segments[0].edge == walk.segments[1].edge)
    )


# This is alg:cycle_removal in the monograph
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
