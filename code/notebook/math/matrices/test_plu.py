from .matrix import FloatMatrix
from .norm import are_close, is_unit
from .plu import plu, plu_inv
from .triangular import is_lower_triangular, is_orthogonal, is_upper_triangular


def test_plu_basic(mat123f: FloatMatrix) -> None:
    p, l, u = plu(mat123f)

    assert is_orthogonal(p)
    assert is_lower_triangular(l)
    assert is_upper_triangular(u)

    assert are_close(mat123f, p @ l @ u)


def test_plu_inv(mat123f: FloatMatrix) -> None:
    assert is_unit(plu_inv(mat123f) @ mat123f)
    assert is_unit(mat123f @ plu_inv(mat123f))
