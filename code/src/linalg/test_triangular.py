from .matrix import Matrix, eye, is_close
from .triangular import lower_triangular_inv


def test_lower_triangular_inv(lower_pascal3: Matrix[int]):
    assert is_close(
        lower_triangular_inv(lower_pascal3) @ lower_pascal3,
        eye(3)
    )

    assert is_close(
        lower_pascal3 @ lower_triangular_inv(lower_pascal3),
        eye(3)
    )
