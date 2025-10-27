from .graph import DirectedGraph
from .opposite import get_opposite_graph


def test_get_opposite_graph() -> None:
    graph = DirectedGraph[int, None, None]()
    graph.edges.add(3, 4)
    assert (3, 4) in graph.edges

    opp = get_opposite_graph(graph)
    assert (3, 4) not in opp.edges
    assert (4, 3) in opp.edges
