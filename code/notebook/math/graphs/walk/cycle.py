from collections.abc import Collection
from typing import cast

from .base import GraphWalkType
from .directed import DirectedWalk


def is_closed[VertT, EdgeT: Collection](walk: GraphWalkType[VertT, EdgeT]) -> bool:
    vertices = list(walk.iter_vertices())

    if len(vertices) == 0:
        return True

    return walk.origin == vertices[-1]


def is_cycle[VertT, EdgeT: Collection](walk: GraphWalkType[VertT, EdgeT]) -> bool:
    it = iter(walk.iter_vertices())
    next(it)
    rest = list(it)

    if len(rest) == 0:
        return False

    if len(list(set(rest))) < len(walk) or len(set(walk.arcs)) < len(walk):
        return False

    return walk.origin == rest[-1]


# This is alg:cycle_removal in the monograph
def remove_cycles[VertT, EdgeT: Collection](walk: DirectedWalk[VertT, EdgeT]) -> DirectedWalk[VertT, EdgeT]:
    if len(walk.arcs) == 0:
        return walk

    current_vertex = walk.origin
    last_compatible_index = 0
    new_walk_arcs = list[EdgeT]()

    while last_compatible_index + 1 < len(walk.arcs):
        for i, (src, _) in enumerate(walk.arcs):
            if src == current_vertex:
                last_compatible_index = i

        arc = walk.arcs[last_compatible_index]
        new_walk_arcs.append(arc)

        _, dest = arc
        current_vertex = cast(VertT, dest)

    return DirectedWalk[VertT, EdgeT](walk.origin, new_walk_arcs)
