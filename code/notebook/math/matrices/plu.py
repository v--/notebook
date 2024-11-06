import functools
import operator

from .matrix import IFieldMatrix, ISemiringMatrix
from .triangular import lower_triangular_inv, upper_triangular_inv


def swapping_matrix[M: ISemiringMatrix](cls: type[M], n: int, j: int, k: int) -> M:
    perm = cls.eye(n)
    perm[j, j] = 0
    perm[k, k] = 0
    perm[j, k] = 1
    perm[k, j] = 1
    return perm


def scaling_matrix[M: ISemiringMatrix](cls: type[M], n: int, i: int, alpha: M) -> M:
    result = cls.eye(n)
    result[i, i] = alpha
    return result


def transvection_matrix[M: ISemiringMatrix](cls: type[M], n: int, i: int, j: int, alpha: M) -> M:
    result = cls.eye(n)
    result[j, i] = alpha
    return result


# This is alg:plu_decomposition in the monograph
def plu[M: IFieldMatrix](a: M) -> tuple[M, M, M]:
    """PLU decomposition done entirely via multiplication of elementary matrices"""
    assert a.is_square()
    cls = type(a)

    l = cls.eye(a.n)
    p = cls.eye(a.n)

    for k in range(a.n - 1):
        u = l @ p @ a

        if all(u[j, k] == 0 for j in range(k + 1, a.n)):
            continue

        perm = swapping_matrix(
            cls,
            a.n,
            min(j for j in range(k + 1, a.n) if u[j, k] != 0),
            k
        )

        p = perm @ p
        u_perm = perm @ u
        l = functools.reduce(
            operator.matmul,
            (transvection_matrix(cls, a.n, k, j, -u_perm[j, k] / u_perm[k, k]) for j in range(k + 1, a.n))
        ) @ perm @ l @ perm

    return (
        p.transpose(),  # The inverse of P is its transpose
        lower_triangular_inv(l),
        l @ p @ a
    )


def plu_inv[M: IFieldMatrix](a: M) -> M:
    assert a.is_square()
    p, l, u = plu(a)
    return upper_triangular_inv(u) @ lower_triangular_inv(l) @ p.transpose()
