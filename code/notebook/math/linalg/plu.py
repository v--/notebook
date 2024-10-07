import functools
import operator
from typing import overload

from .dtypes import field_of
from .matrix import Matrix, eye
from .triangular import lower_triangular_inv, upper_triangular_inv


a: int = 3

def swapping_matrix(n: int, j: int, k: int) -> Matrix[int]:
    perm = eye(n)
    perm[j, j] = 0
    perm[k, k] = 0
    perm[j, k] = 1
    perm[k, j] = 1
    return perm


def scaling_matrix[N: (int, float, complex)](n: int, i: int, alpha: N) -> Matrix[N]:
    result = eye(n, dtype=type(alpha))
    result[i, i] = alpha
    return result


def transvection_matrix[N: (int, float, complex)](n: int, i: int, j: int, alpha: N) -> Matrix[N]:
    result = eye(n, dtype=type(alpha))
    result[j, i] = alpha
    return result


# This is alg:plu_decomposition in the monograph
@overload
def plu(a: Matrix[int]) -> tuple[Matrix[int], Matrix[float], Matrix[float]]: ...
@overload
def plu[N: (float, complex)](a: Matrix[N]) -> tuple[Matrix[int], Matrix[N], Matrix[N]]: ...
def plu(a: Matrix) -> tuple[Matrix[int], Matrix, Matrix]:
    """PLU decomposition done entirely via multiplication of elementary matrices"""
    assert a.is_square()

    l = eye(a.n, dtype=field_of(a.dtype))
    p = eye(a.n)

    for k in range(a.n - 1):
        u = l @ p @ a

        if all(u[j, k] == 0 for j in range(k + 1, a.n)):
            continue

        perm = swapping_matrix(
            a.n,
            min(j for j in range(k + 1, a.n) if u[j, k] != 0),
            k
        )

        p = perm @ p
        u_perm = perm @ u
        l = functools.reduce(
            operator.matmul,
            (transvection_matrix(a.n, k, j, -u_perm[j, k] / u_perm[k, k]) for j in range(k + 1, a.n))
        ) @ perm @ l @ perm

    return (
        p.transpose(),  # The inverse of P is its transpose
        lower_triangular_inv(l),
        l @ p @ a
    )

@overload
def plu_inv(a: Matrix[int]) -> Matrix[float]: ...
@overload
def plu_inv[N: (float, complex)](a: Matrix[N]) -> Matrix[N]: ...
def plu_inv(a: Matrix) -> Matrix:
    assert a.is_square()
    p, l, u = plu(a)
    return upper_triangular_inv(u) @ lower_triangular_inv(l) @ p.transpose()
