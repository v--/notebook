from typing import overload

from .dtypes import F, N, field_of
from .matrix import Matrix, convert_dtype, eye, is_close


def is_orthogonal(l: Matrix[N]) -> bool:
    assert l.is_square()
    return is_close(l @ l.transpose(), eye(l.n)) and is_close(l.transpose() @ l, eye(l.n))


def is_lower_triangular(l: Matrix[N]) -> bool:
    return all(
        l[i, j] == 0
        for i in range(1, l.m)
        for j in range(min(i, l.n) + 1, l.n)
    )


@overload
def lower_triangular_inv(l: Matrix[int], dtype: type[int] = int) -> Matrix[float]: ...
@overload
def lower_triangular_inv(l: Matrix[F], dtype: type[F] = float) -> Matrix[F]: ...
def lower_triangular_inv(l: Matrix[N], dtype: type[N] = int) -> Matrix:
    assert l.is_square()
    assert is_lower_triangular(l)

    t = convert_dtype(l, field_of(dtype))
    r: Matrix = eye(l.n, dtype=field_of(dtype))

    for j in range(l.n - 1, -1, -1):
        r[j, :] = r[j, :] / t[j, j]
        t[j, :] = t[j, :] / t[j, j]

        for i in range(j + 1, l.n):
            r[i, :] -= t[i, j] * r[j, :]
            t[i, :] -= t[i, j] * t[j, :]

    return r


def is_upper_triangular(l: Matrix[N]) -> bool:
    return all(
        l[i, j] == 0
        for i in range(1, l.m)
        for j in range(min(i, l.n))
    )


@overload
def upper_triangular_inv(l: Matrix[int], dtype: type[int]) -> Matrix[float]: ...
@overload
def upper_triangular_inv(l: Matrix[F], dtype: type[F]) -> Matrix[F]: ...
def upper_triangular_inv(l: Matrix[N], dtype: type[N] = int):
    return lower_triangular_inv(l.transpose(), dtype=dtype).transpose()
