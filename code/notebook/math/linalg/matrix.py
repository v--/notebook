import functools
import operator
from collections.abc import Iterable
from typing import cast, overload

from .exceptions import LinAlgError


class MatrixError(LinAlgError):
    pass


class Matrix[N: (int, float, complex)]:
    m: int
    n: int
    payload: list[N]
    dtype: type[N]

    def __init__(self, rows: list[list[N]], dtype: type[N] | None = None) -> None:
        for row in rows:
            assert len(row) == len(rows[0])

        self.m = len(rows)
        self.n = len(rows[0]) if len(rows) > 0 else 0
        self.payload = [x for row in rows for x in row]

        if dtype is None:
            if len(self.payload) == 0:
                raise MatrixError('Cannot infer dtype without any data')

            dtype = type(self.payload[0])

        self.dtype = dtype

    def __i_range(self, i: int | slice) -> Iterable[int]:
        if isinstance(i, int):
            return [i]

        return range(i.stop or self.m)[i]

    def __j_range(self, j: int | slice) -> Iterable[int]:
        if isinstance(j, int):
            return [j]

        return range(j.stop or self.n)[j]

    @overload
    def __getitem__(self, key: tuple[int, int]) -> 'N': ...
    @overload
    def __getitem__(self, key: tuple[int, slice]) -> 'Matrix[N]': ...
    @overload
    def __getitem__(self, key: tuple[slice, int]) -> 'Matrix[N]': ...
    @overload
    def __getitem__(self, key: tuple[slice, slice]) -> 'Matrix[N]': ...
    def __getitem__(self, key: tuple[int | slice, int | slice]) -> 'N | Matrix[N]':
        i, j = key

        if isinstance(i, int) and isinstance(j, int):
            if i >= self.m or i < -self.m:
                raise IndexError(f'Attempted to access row {i}, but the matrix has only {self.m} rows')

            if j >= self.n or j < -self.n:
                raise IndexError(f'Attempted to access row {j}, but the matrix has only {self.n} rows')

            return self.payload[(i % self.m) * self.n + (j % self.n)]

        return Matrix([
            [self[i_, j_] for j_ in self.__j_range(j)]
            for i_ in self.__i_range(i)
        ])

    def __setitem_islice(self, i: slice, j: int, value: 'N | list[N] | Matrix[N]') -> None:
        i_range = list(self.__i_range(i))

        if isinstance(value, list):
            if len(value) == len(i_range):
                for i_ in i_range:
                    self[i_, j] = value[i_]
            else:
                raise ValueError(f'List of length {len(value)} does not fit in {len(i_range)} places')

        elif isinstance(value, Matrix):
            if value.m == len(i_range) and value.n == 1:
                for i_ in i_range:
                    self[i_, j] = value[i_, 0]
            else:
                raise ValueError(f'Matrix of size {value.m}×{value.n} does not fit in {len(i_range)} places')

        else:
            for i_ in i_range:
                self[i_, j] = value

    def __setitem_jslice(self, i: int, j: slice, value: 'N | list[N] | Matrix[N]') -> None:
        j_range = list(self.__j_range(j))

        if isinstance(value, list):
            if len(value) == len(j_range):
                for j_ in j_range:
                    self[i, j_] = value[j_]
            else:
                raise ValueError(f'List of length {len(value)} does not fit in {len(j_range)} places')

        elif isinstance(value, Matrix):
            if value.m == 1 and value.n == len(j_range):
                for j_ in j_range:
                    self[i, j_] = value[0, j_]
            else:
                raise ValueError(f'Matrix of size {value.m}×{value.n} does not fit in {len(j_range)} places')

        else:
            for j_ in j_range:
                self[i, j_] = value

    def __setitem_slices(self, i: slice, j: slice, value: 'N | list[N] | Matrix[N]') -> None:
        i_range = list(self.__i_range(i))
        j_range = list(self.__j_range(j))

        if isinstance(value, list):
            raise TypeError('Cannot assign a list onto a matrix')

        if isinstance(value, Matrix):
            if value.m == len(i_range) and value.n == len(j_range):
                for i_ in i_range:
                    for j_ in j_range:
                        self[i_, j_] = value[i_, j_]
            else:
                raise ValueError(f'Matrix of size {value.m}×{value.n} does not fit in {len(i_range)}×{len(j_range)} places')

        else:
            for i_ in i_range:
                for j_ in j_range:
                    self[i_, j_] = value

    @overload
    def __setitem__(self, key: tuple[int, int], value: N) -> None: ...
    @overload
    def __setitem__(self, key: tuple[int, slice], value: 'N | list[N] | Matrix[N]') -> None: ...
    @overload
    def __setitem__(self, key: tuple[slice, int], value: 'N | list[N] | Matrix[N]') -> None: ...
    @overload
    def __setitem__(self, key: tuple[slice, slice], value: 'N | Matrix[N]') -> None: ...
    def __setitem__(self, key: tuple[int | slice, int | slice], value: 'N | list[N] | Matrix[N]') -> None:
        i, j = key

        if isinstance(i, slice) and isinstance(j, slice):
            self.__setitem_slices(i, j, value)
        elif isinstance(i, slice) and isinstance(j, int):
            self.__setitem_islice(i, j, value)
        elif isinstance(i, int) and isinstance(j, slice):
            self.__setitem_jslice(i, j, value)
        elif isinstance(i, int) and isinstance(j, int):
            if i >= self.m or i < -self.m:
                raise IndexError(f'Attempted to access row {i}, but the matrix has only {self.m} rows')

            if j >= self.n or j < -self.n:
                raise IndexError(f'Attempted to access row {j}, but the matrix has only {self.n} rows')

            self.payload[(i % self.m) * self.n + (j % self.n)] = cast(N, value)

    def get_rows(self) -> list[list[N]]:
        return [
            [self[i, j] for j in range(self.n)]
            for i in range(self.m)
        ]

    def get_cols(self) -> list[list[N]]:
        return [
            [self[i, j] for i in range(self.m)]
            for j in range(self.n)
        ]

    def is_square(self) -> bool:
        return self.m == self.n

    def transpose(self) -> 'Matrix[N]':
        return Matrix(self.get_cols())

    def __str__(self) -> str:
        return '|' + '|\n|'.join('\t'.join(map(str, row)) for row in self.get_rows()) + '|'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented

        return self.payload == other.payload

    def __neg__(self) -> 'Matrix[N]':
        return Matrix([
            [cast(N, -x) for x in row]
            for row in self.get_rows()
        ])

    @overload
    def __add__(self, other: 'Matrix[N]') -> 'Matrix[N]': ...
    @overload
    def __add__(self, other: 'Matrix[int]') -> 'Matrix[N]': ...
    @overload
    def __add__(self, other: 'Matrix[complex]') -> 'Matrix[complex]': ...
    @overload
    def __add__(self: 'Matrix[int] | Matrix[float]', other: 'Matrix[float]') -> 'Matrix[float]': ...
    @overload
    def __add__[M: (int, float, complex)](self: 'Matrix[complex]', other: 'Matrix[M]') -> 'Matrix[complex]': ...
    def __add__(self, other: object):
        if not isinstance(other, Matrix) or self.m != other.m or self.n != other.n:
            return NotImplemented

        return Matrix([
            [x + y for x, y in zip(row_a, row_b, strict=True)]
            for row_a, row_b in zip(self.get_rows(), other.get_rows(), strict=True)
        ])

    @overload
    def __sub__(self, other: 'Matrix[N]') -> 'Matrix[N]': ...
    @overload
    def __sub__(self, other: 'Matrix[int]') -> 'Matrix[N]': ...
    @overload
    def __sub__(self, other: 'Matrix[complex]') -> 'Matrix[complex]': ...
    @overload
    def __sub__(self: 'Matrix[int] | Matrix[float]', other: 'Matrix[float]') -> 'Matrix[float]': ...
    @overload
    def __sub__[M: (int, float, complex)](self: 'Matrix[complex]', other: 'Matrix[M]') -> 'Matrix[complex]': ...
    def __sub__(self, other: object):
        if not isinstance(other, Matrix) or self.m != other.m or self.n != other.n:
            return NotImplemented

        return self + (-other)

    @overload
    def __rmul__(self, other: N) -> 'Matrix[N]': ...
    @overload
    def __rmul__(self, other: complex) -> 'Matrix[complex]': ...
    @overload
    def __rmul__(self: 'Matrix[int] | Matrix[float]', other: float) -> 'Matrix[float]': ...
    def __rmul__(self, other: object) -> 'Matrix':
        if not isinstance(other, int | float | complex):
            return NotImplemented

        return Matrix([
            [other * x for x in row]
            for row in self.get_rows()
        ])

    @overload
    def __truediv__(self, other: N) -> 'Matrix[N]': ...
    @overload
    def __truediv__(self, other: complex) -> 'Matrix[complex]': ...
    @overload
    def __truediv__(self: 'Matrix[int] | Matrix[float]', other: float) -> 'Matrix[float]': ...
    def __truediv__(self, other: object) -> 'Matrix':
        if not isinstance(other, int | float | complex):
            return NotImplemented

        return (1 / other) * self

    @overload
    def __matmul__(self, other: 'Matrix[N]') -> 'Matrix[N]': ...
    @overload
    def __matmul__(self, other: 'Matrix[int]') -> 'Matrix[N]': ...
    @overload
    def __matmul__(self, other: 'Matrix[complex]') -> 'Matrix[complex]': ...
    @overload
    def __matmul__(self: 'Matrix[int] | Matrix[float]', other: 'Matrix[float]') -> 'Matrix[float]': ...
    @overload
    def __matmul__[M: (int, float, complex)](self: 'Matrix[complex]', other: 'Matrix[M]') -> 'Matrix[complex]': ...
    def __matmul__(self, other: object) -> 'Matrix':
        if not isinstance(other, Matrix) or self.n != other.m:
            return NotImplemented

        return Matrix([
            [
                # We avoid using sum since it starts at zero, perplexing tropical arithmetic
                functools.reduce(operator.add, (x * y for x, y in zip(row, col, strict=True)))
                for col in other.get_cols()
            ]
            for row in self.get_rows()
        ])


def convert_dtype[M: (int, float, complex)](src: Matrix, dtype: type[M]) -> Matrix[M]:
    return Matrix([
        [dtype(cell) for cell in row]
        for row in src.get_rows()
    ])


def fill[N: (int, float, complex)](n: int, m: int | None = None, dtype: type[N] = int, value: N = 0) -> Matrix[N]:
    assert n >= 0

    if m is not None:
        assert m >= 0

    return Matrix([
        [dtype(value) for j in range(m or n)]
        for i in range(n)
    ])


def eye[N: (int, float, complex)](n: int, m: int | None = None, dtype: type[N] = int, diag: N = 1, off_diag: N = 0) -> Matrix[N]:
    result = fill(n, m, dtype, off_diag)

    for i in range(min(result.n, result.m)):
        result[i, i] = dtype(diag)

    return result


def ones[N: (int, float, complex)](n: int, m: int | None = None, dtype: type[N] = int) -> Matrix[N]:
    return fill(n, m, dtype, 1)


def zeros[N: (int, float, complex)](n: int, m: int | None = None, dtype: type[N] = int) -> Matrix[N]:
    return fill(n, m, dtype, 0)


def is_close(a: Matrix, b: Matrix, tolerance: float = 1e-10) -> bool:
    assert a.m == b.m
    assert a.n == b.n

    for i in range(a.m):
        for j in range(a.n):
            if abs(a[i, j] - b[i, j]) > tolerance:
                return False

    return True
