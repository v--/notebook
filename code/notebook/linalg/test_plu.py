from .matrix import Matrix, is_close
from .triangular import is_lower_triangular, is_orthogonal, is_upper_triangular
from .matrix import eye
from .plu import plu, plu_inv


def test_plu_basic(mat123: Matrix[int]):
    p, l, u = plu(mat123)

    assert is_orthogonal(p)
    assert is_lower_triangular(l)
    assert is_upper_triangular(u)

    assert is_close(mat123, p @ l @ u)


def test_plu_inv(mat123: Matrix[int]):
    assert is_close(
        plu_inv(mat123) @ mat123,
        eye(3)
    )

    assert is_close(
        mat123 @ plu_inv(mat123),
        eye(3)
    )
