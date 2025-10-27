from .logical import LogicalMatrix


def test_logical_matrix_addition() -> None:
    eye = LogicalMatrix.eye(3)
    zero = LogicalMatrix.zeros(3)
    assert eye + eye == zero

