import functools
import operator
from typing import TypeVar

from .matrix import Matrix, eye
from .triangular import lower_triangular_inv, upper_triangular_inv


def swapping_matrix(n: int, j: int, k: int):
    perm = eye(n)
    perm[j, j] = 0
    perm[k, k] = 0
    perm[j, k] = 1
    perm[k, j] = 1
    return perm


def scaling_matrix(n: int, i: int, alpha: float):
    result = eye(n)
    result[i, i] = alpha
    return result


def transvection_matrix(n: int, i: int, j: int, alpha: float):
    result = eye(n)
    result[j, i] = alpha
    return result


N = TypeVar('N', bound=int | float)


# PLU decomposition done entirely via multiplication of elementary matrices
# alg:plu_decomposition
def plu(a: Matrix[N]) -> tuple[Matrix[N], Matrix[N], Matrix[N]]:
    assert a.is_square()

    l = eye(a.n)
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


def plu_inv(a: Matrix[N]) -> Matrix[N]:
    assert a.is_square()
    p, l, u = plu(a)
    return upper_triangular_inv(u) @ lower_triangular_inv(l) @ p.transpose()
