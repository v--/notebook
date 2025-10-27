from .directed_multi import DirectedMultiedge, DirectedMultigraph


def test_add_parallel_edges() -> None:
    graph = DirectedMultigraph[int, None, None]()

    e1 = DirectedMultiedge(3, 4)
    e2 = DirectedMultiedge(3, 4)

    graph.edges.add(e1)
    graph.edges.add(e2)

    assert [e1, e2] == list(graph.edges)
