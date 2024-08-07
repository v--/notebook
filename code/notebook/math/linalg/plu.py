import functools
import operator
from typing import TypeVar

from .dtypes import field_of
from .matrix import Matrix, eye
from .triangular import lower_triangular_inv, upper_triangular_inv


N = TypeVar('N', int, float, complex)
F = TypeVar('F', float, complex)


def swapping_matrix(n: int, j: int, k: int, dtype: type[N] = int) -> Matrix[N]:
    perm = eye(n, dtype=dtype)
    perm[j, j] = 0
    perm[k, k] = 0
    perm[j, k] = 1
    perm[k, j] = 1
    return perm


def scaling_matrix(n: int, i: int, alpha: N, dtype: type[N] = int) -> Matrix[N]:
    result = eye(n, dtype=dtype)
    result[i, i] = alpha
    return result


def transvection_matrix(n: int, i: int, j: int, alpha: N, dtype: type[N] = int) -> Matrix[N]:
    result = eye(n, dtype=dtype)
    result[j, i] = alpha
    return result


# PLU decomposition done entirely via multiplication of elementary matrices
# alg:plu_decomposition
def plu(a: Matrix[F] | Matrix[int], dtype: type[F | int] = int) -> tuple[Matrix[int], Matrix[F], Matrix[F]]:
    assert a.is_square()

    l = eye(a.n, dtype=field_of(dtype))
    p = eye(a.n, dtype=int)

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
            (transvection_matrix(a.n, k, j, -u_perm[j, k] / u_perm[k, k], dtype=dtype) for j in range(k + 1, a.n))
        ) @ perm @ l @ perm

    return (
        p.transpose(),  # The inverse of P is its transpose
        lower_triangular_inv(l),
        l @ p @ a
    )


def plu_inv(a: Matrix[F] | Matrix[int], dtype: type[F | int] = int) -> Matrix[F]:
    assert a.is_square()
    p, l, u = plu(a, dtype=dtype)
    return upper_triangular_inv(u, dtype=dtype) @ lower_triangular_inv(l, dtype=dtype) @ p.transpose()
