from typing import TypeVar, Generic, cast


N = TypeVar('N', bound=int | float)


class Matrix(Generic[N]):
    m: int
    n: int
    payload: list[N]

    def __init__(self, rows: list[list[N]]):
        for row in rows:
            assert len(row) == len(rows[0])

        self.m = len(rows)
        self.n = len(rows[0])
        self.payload = [x for row in rows for x in row]

    def __i_range(self, i: int | slice):
        if isinstance(i, int):
            return [i]

        return range(i.stop or self.m)[i]

    def __j_range(self, j: int | slice):
        if isinstance(j, int):
            return [j]

        return range(j.stop or self.n)[j]

    def __getitem__(self, key: tuple[int | slice, int | slice]):
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

    def __setitem_islice(self, i: slice, j: int, value: N | list[N] | 'Matrix[N]'):
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
                self[i, i_] = value

    def __setitem_jslice(self, i: int, j: slice, value: N | list[N] | 'Matrix[N]'):
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

    def __setitem_slices(self, i: slice, j: slice, value: N | list[N] | 'Matrix[N]'):
        i_range = list(self.__i_range(i))
        j_range = list(self.__j_range(j))

        if isinstance(value, list):
            raise ValueError('Cannot assign a list onto a matrix')

        elif isinstance(value, Matrix):
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

    def __setitem__(self, key: tuple[int | slice, int | slice], value: N | list[N] | 'Matrix[N]'):
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

            if isinstance(value, int | float):
                self.payload[(i % self.m) * self.n + (j % self.n)] = cast(N, value)
            else:
                raise ValueError(f'Invalid scalar value {repr(value)}')

    def get_rows(self):
        return [
            [self[i, j] for j in range(self.n)]
            for i in range(self.m)
        ]

    def get_cols(self):
        return [
            [self[i, j] for i in range(self.m)]
            for j in range(self.n)
        ]

    def is_square(self):
        return self.m == self.n

    def transpose(self):
        return Matrix(self.get_cols())

    def __str__(self):
        return '|' + '|\n|'.join('\t'.join(map(str, row)) for row in self.get_rows()) + '|'

    def __eq__(self, other: object):
        if not isinstance(other, Matrix):
            return NotImplemented

        return self.payload == other.payload

    def __neg__(self):
        return Matrix([
            [-x for x in row]
            for row in self.get_rows()
        ])

    def __add__(self, other: object):
        if not isinstance(other, Matrix) or self.m != other.m or self.n != other.n:
            return NotImplemented

        return Matrix([
            [x + y for x, y in zip(row_a, row_b)]
            for row_a, row_b in zip(self.get_rows(), other.get_rows())
        ])

    def __sub__(self, other: object):
        if not isinstance(other, Matrix) or self.m != other.m or self.n != other.n:
            return NotImplemented

        return self + (-other)

    def __mul__(self, other: object):
        if not isinstance(other, int | float):
            return NotImplemented

        return Matrix([
            [other * x for x in row]
            for row in self.get_rows()
        ])

    def __truediv__(self, other: object):
        if not isinstance(other, int | float):
            return NotImplemented

        return self * (1 / other)

    def __matmul__(self, other: object):
        if not isinstance(other, Matrix) or self.n != other.m:
            return NotImplemented

        return Matrix([
            [
                sum(x * y for x, y in zip(row, col))
                for col in other.get_cols()
            ]
            for row in self.get_rows()
        ])


def eye(n: int):
    return Matrix([
        [1 if i == j else 0 for j in range(n)]
        for i in range(n)
    ])


def zeros(n: int):
    return Matrix([
        [0 for _ in range(n)]
        for _ in range(n)
    ])


def is_close(a: Matrix[N], b: Matrix[N], tolerance: float = 1e-3):
    assert a.m == b.m
    assert a.n == b.n

    for i in range(a.m):
        for j in range(a.n):
            if abs(a[i, j] - b[i, j]) > tolerance:
                return False

    return True
