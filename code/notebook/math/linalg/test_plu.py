from .matrix import Matrix, eye, is_close
from .plu import plu, plu_inv
from .triangular import is_lower_triangular, is_orthogonal, is_upper_triangular


def test_plu_basic(mat123: Matrix[int]) -> None:
    p, l, u = plu(mat123)

    assert is_orthogonal(p)
    assert is_lower_triangular(l)
    assert is_upper_triangular(u)

    assert is_close(mat123, p @ l @ u)


def test_plu_inv(mat123: Matrix[float]) -> None:
    e = eye(3)
    assert is_close(plu_inv(mat123) @ mat123, e)
    assert is_close(mat123 @ plu_inv(mat123), e)
