from .graph import DirectedGraph


def get_opposite_graph[T: DirectedGraph](graph: T) -> T:
    opp = graph.clone_initial()

    for vertex, label in graph.vertices.get_labeled():
        opp.vertices[vertex] = label

    for (src, dest), label in graph.edges.get_labeled():
        opp.edges[dest, src] = label

    return opp
