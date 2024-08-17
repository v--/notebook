from typing import cast

from .generalized import GeneralizedArcT, VertT
from .walk import DirectedWalk, GraphWalk


def is_closed(walk: GraphWalk[VertT, GeneralizedArcT]) -> bool:
    vertices = list(walk.iter_vertices())

    if len(vertices) == 0:
        return True

    return walk.origin == vertices[-1]


def is_cycle(walk: GraphWalk[VertT, GeneralizedArcT]) -> bool:
    it = iter(walk.iter_vertices())
    next(it)
    rest = list(it)

    if len(rest) == 0:
        return False

    if len(list(set(rest))) < len(walk) or len(set(walk.arcs)) < len(walk):
        return False

    return walk.origin == rest[-1]


# This is alg:cycle_removal in the monograph
def remove_cycles(walk: DirectedWalk[VertT, GeneralizedArcT]) -> DirectedWalk[VertT, GeneralizedArcT]:
    if len(walk.arcs) == 0:
        return walk

    new_walk: DirectedWalk[VertT, GeneralizedArcT] = DirectedWalk(walk.origin, [])
    current_vertex = walk.origin
    last_compatible_index = 0

    while last_compatible_index + 1 < len(walk.arcs):
        for i, (src, _) in enumerate(walk.arcs):
            if src == current_vertex:
                last_compatible_index = i

        arc = walk.arcs[last_compatible_index]
        new_walk.arcs.append(arc)

        _, dest = arc
        current_vertex = cast(VertT, dest)

    return new_walk
