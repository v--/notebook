from .matrix import FloatMatrix, IFieldMatrix, ISemiringMatrix
from .norm import is_unit


def is_orthogonal(mat: FloatMatrix) -> bool:
    assert mat.is_square()
    return is_unit(mat @ mat.transpose()) and is_unit(mat.transpose() @ mat)


def is_lower_triangular[M: ISemiringMatrix](mat: M) -> bool:
    return all(
        mat[i, j] == 0
        for i in range(1, mat.m)
        for j in range(min(i, mat.n) + 1, mat.n)
    )


def lower_triangular_inv[M: IFieldMatrix](mat: M) -> M:
    assert mat.is_square()
    assert is_lower_triangular(mat)

    l = mat[:, :]
    r = mat.eye(mat.n)

    for j in range(mat.n - 1, -1, -1):
        r[j, :] = r[j, :] / l[j, j]
        l[j, :] = l[j, :] / l[j, j]

        for i in range(j + 1, mat.n):
            r[i, :] -= l[i, j] * r[j, :]
            l[i, :] -= l[i, j] * l[j, :]

    return r


def is_upper_triangular[M: ISemiringMatrix](mat: M) -> bool:
    return all(
        mat[i, j] == 0
        for i in range(1, mat.m)
        for j in range(min(i, mat.n))
    )


def upper_triangular_inv[M: IFieldMatrix](mat: M) -> M:
    return lower_triangular_inv(mat.transpose()).transpose()
