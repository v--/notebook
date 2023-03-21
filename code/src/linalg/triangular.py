from typing import TypeVar
from numbers import Number

from .matrix import Matrix, eye, is_close


N = TypeVar('N', bound=Number)


def is_orthogonal(l: Matrix[N]):
    assert l.is_square()
    return is_close(l @ l.transpose(), eye(l.n)) and is_close(l.transpose() @ l, eye(l.n))


def is_lower_triangular(l: Matrix[N]):
    return all(
        l[i, j] == 0
        for i in range(1, l.m)
        for j in range(min(i, l.n) + 1, l.n)
    )


def lower_triangular_inv(l: Matrix[N]) -> Matrix[N]:
    assert l.is_square()
    assert is_lower_triangular(l)

    t = l[:, :]
    r = eye(l.n)

    for j in range(l.n - 1, -1, -1):
        r[j, :] = r[j, :] / t[j, j]
        t[j, :] = t[j, :] / t[j, j]

        for i in range(j + 1, l.n):
            r[i, :] -= r[j, :] * t[i, j]
            t[i, :] -= t[j, :] * t[i, j]

    return r


def is_upper_triangular(l: Matrix[N]):
    return all(
        l[i, j] == 0
        for i in range(1, l.m)
        for j in range(min(i, l.n))
    )


def upper_triangular_inv(l: Matrix[N]) -> Matrix[N]:
    return lower_triangular_inv(l.transpose()).transpose()
