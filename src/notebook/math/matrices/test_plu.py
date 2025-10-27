from .matrix import FloatMatrix, IntMatrix
from .norm import are_close, is_unit
from .plu import plu, plu_inv
from .triangular import is_lower_triangular, is_orthogonal, is_upper_triangular


def test_plu_basic(mat123f: FloatMatrix) -> None:
    p, l, u = plu(mat123f)

    assert is_orthogonal(p)
    assert is_lower_triangular(l, unitriangular=True)
    assert is_upper_triangular(u)

    assert are_close(mat123f, p @ l @ u)


def test_plu_basic2() -> None:
    m = FloatMatrix.from_rows([
        [1, 0, 3],
        [1, 0, 3],
        [3, 2, 1],
    ])

    p, l, u = plu(m)

    assert is_orthogonal(p)
    assert is_lower_triangular(l, unitriangular=True)
    assert is_upper_triangular(u)


def test_plu_inv(mat123f: FloatMatrix) -> None:
    assert is_unit(plu_inv(mat123f) @ mat123f)
    assert is_unit(mat123f @ plu_inv(mat123f))


# ex:def:group_commutator/gl2
def test_commutator_example() -> None:
    a = IntMatrix.from_rows([[1, 1], [0, 1]])
    b = IntMatrix.from_rows([[1, 1], [1, 0]])

    ab = IntMatrix.from_rows([[2, 1], [1, 0]])
    ba = IntMatrix.from_rows([[1, 2], [1, 1]])

    comm = IntMatrix.from_rows([[-1, 3], [-1, 2]])

    assert a @ b == ab
    assert b @ a == ba

    assert ab @ plu_inv(FloatMatrix.lift_matrix(ba)).round() == comm
