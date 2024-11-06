from .matrix import FloatMatrix, IntMatrix
from .norm import is_unit
from .triangular import lower_triangular_inv


def test_lower_triangular_inv(lower_pascal3: IntMatrix) -> None:
    mat = FloatMatrix.lift_matrix(lower_pascal3)

    assert is_unit(lower_triangular_inv(mat) @ mat)
    assert is_unit(mat @ lower_triangular_inv(mat))
