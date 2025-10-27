from .base import linearize_index


def test_linearize_index() -> None:
    assert linearize_index(dimensions=[], indices=[]) == 0
    assert linearize_index(dimensions=[10], indices=[5]) == 5
    assert linearize_index(dimensions=[10, 5], indices=[5, 3]) == 28
    assert linearize_index(dimensions=[10, 5, 9], indices=[5, 3, 8]) == 260
