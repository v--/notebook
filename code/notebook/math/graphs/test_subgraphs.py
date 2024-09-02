import pytest

from .complete import complete_graph
from .subgraphs import (
    enumerate_fixed_order_subgraphs,
    enumerate_subgraphs,
    max_fixed_order_subgraph_count,
    max_subgraph_count,
)


@pytest.mark.parametrize('n', list(range(2, 6)))
def test_enumerate_fixed_order_subgraphs_complete(n: int) -> None:
    for k in range(n):
        subgraphs = list(enumerate_fixed_order_subgraphs(complete_graph(n), order=k))
        assert len(subgraphs) == max_fixed_order_subgraph_count(n, k)


@pytest.mark.parametrize('n', list(range(2, 6)))
def test_enumerate_subgraphs_complete(n: int) -> None:
    assert len(enumerate_subgraphs(complete_graph(n))) == max_subgraph_count(n)
