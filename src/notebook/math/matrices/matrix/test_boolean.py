from .boolean import BooleanMatrix


def test_boolean_matrix_addition() -> None:
    eye = BooleanMatrix.eye(3)
    zero = BooleanMatrix.zeros(3)
    assert eye + eye == zero

