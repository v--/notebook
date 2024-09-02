import random

import pytest

from .complete import complete_graph, is_complete


@pytest.mark.parametrize('k', [random.randint(0, 10) for _ in range(5)])
def test_complete_graph(k: int) -> None:
    assert is_complete(complete_graph(k))
