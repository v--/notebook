from .multi import DirectedMultigraph, MultiArc, MultiEdge, UndirectedMultigraph


def test_directed_arcs() -> None:
    graph: DirectedMultigraph[str] = DirectedMultigraph()

    arc1 = MultiArc('a', 'b')
    arc2 = MultiArc('a', 'b')

    assert arc1 != arc2

    graph.arcs.add(arc1)
    graph.arcs.add(arc2)

    assert len(graph.arcs) == 2


def test_undirected_arcs() -> None:
    graph: UndirectedMultigraph[str] = UndirectedMultigraph()

    edge1 = MultiEdge('a', 'b')
    edge2 = MultiEdge('a', 'b')

    assert edge1 != edge2

    graph.edges.add(edge1)
    graph.edges.add(edge2)

    assert len(graph.edges) == 2
