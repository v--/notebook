import random

from ...support.pytest import pytest_parametrize_lists, repeat5
from .complete import complete_graph, is_complete


@pytest_parametrize_lists(k=repeat5(random.randint, 0, 10))
def test_complete_graph(k: int) -> None:
    assert is_complete(complete_graph(k))
