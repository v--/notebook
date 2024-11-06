import functools
import operator
from collections.abc import Callable, Iterable, Iterator, Sequence
from enum import StrEnum
from typing import Any, Self, cast, overload

from ....support.iteration import string_accumulator
from ...rings.arithmetic import IField, IRing, ISemiring
from .exceptions import MatrixIndexError, MatrixValueError


class SpecialChars(StrEnum):
    single_left = '('
    single_right = ')'
    upper_left = '⎛'
    lower_left = '⎝'
    upper_right = '⎞'
    lower_right = '⎠'
    pipe = '⎜'


def linearize_index(dimensions: Iterable[int], indices: Iterable[int]) -> int:
    result = 0

    for index, dim in zip(indices, dimensions, strict=True):
        assert dim >= 0
        result *= dim
        result += index % dim  # We thus support negative indexing

    return result


class MatrixMeta(type):
    semiring: type[ISemiring]

    def __new__[M: MatrixMeta](
        meta: type[M],  # noqa: N804
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        semiring: type[ISemiring] = ISemiring,
    ) -> M:  # noqa: PYI019
        attrs['semiring'] = semiring
        return type.__new__(meta, name, bases, attrs)


class BaseMatrix[N: ISemiring](metaclass=MatrixMeta):
    m: int
    n: int
    payload: list[N]

    @classmethod
    def lift_to_scalar(cls, value: int) -> N:
        return cast(N, cls.semiring(value))

    @classmethod
    def from_factory(cls, m: int, n: int, factory: Callable[[int, int], N]) -> Self:
        return cls(m, n, factory)

    def __init__(self, m: int, n: int, factory: Callable[[int, int], N] | None = None) -> None:
        assert m >= 0
        assert n >= 0
        self.m = m
        self.n = n
        self.payload = [
            factory(i, j) if factory else self.lift_to_scalar(0)
            for i in range(m)
            for j in range(n)
        ]

    @property
    def dimensions(self) -> tuple[int, int]:
        return (self.m, self.n)

    def __i_range(self, i: int | slice) -> Iterable[int]:
        if isinstance(i, int):
            return [i]

        return range(i.stop if i.stop is not None else self.m)[i]

    def __j_range(self, j: int | slice) -> Iterable[int]:
        if isinstance(j, int):
            return [j]

        return range(j.stop if j.stop is not None else self.n)[j]

    @overload
    def __getitem__(self, key: tuple[int, int]) -> N: ...
    @overload
    def __getitem__(self, key: tuple[int, slice]) -> Self: ...
    @overload
    def __getitem__(self, key: tuple[slice, int]) -> Self: ...
    @overload
    def __getitem__(self, key: tuple[slice, slice]) -> Self: ...
    def __getitem__(self, key: tuple[int | slice, int | slice]) -> N | Self:
        match key:
            case int(), int():
                i, j = key

                if i >= self.m or i < -self.m:
                    raise MatrixIndexError(f'Attempted to access row with index {i}, but the matrix has only {self.m} rows')

                if j >= self.n or j < -self.n:
                    raise MatrixIndexError(f'Attempted to access column with index {j}, but the matrix has only {self.n} columns')

                return self.payload[linearize_index(self.dimensions, key)]

            case _:
                i_range = list(self.__i_range(key[0]))
                j_range = list(self.__j_range(key[1]))

                return self.from_factory(
                    len(i_range),
                    len(j_range),
                    lambda i, j: self[i_range[i], j_range[j]]
                )

    def __setitem_islice(self, i: slice, j: int, value: N | Sequence[N] | Self) -> None:
        i_range = list(self.__i_range(i))

        if isinstance(value, Sequence):
            if len(value) == len(i_range):
                for i_, v in zip(i_range, value, strict=True):
                    self[i_, j] = v
            else:
                raise MatrixValueError(f'List of length {len(value)} does not fit in {len(i_range)} places')

        elif isinstance(value, BaseMatrix):
            if value.m == len(i_range) and value.n == 1:
                for k, i_ in enumerate(i_range):
                    self[i_, j] = value[k, 0]
            else:
                raise MatrixValueError(f'Matrix of size {value.m}×{value.n} does not fit in {len(i_range)} places')

        else:
            for i_ in i_range:
                self[i_, j] = value

    def __setitem_jslice(self, i: int, j: slice, value: N | Sequence[N] | Self) -> None:
        j_range = list(self.__j_range(j))

        if isinstance(value, Sequence):
            if len(value) == len(j_range):
                for j_, v in zip(j_range, value, strict=True):
                    self[i, j_] = v
            else:
                raise MatrixValueError(f'List of length {len(value)} does not fit in {len(j_range)} places')

        elif isinstance(value, BaseMatrix):
            if value.m == 1 and value.n == len(j_range):
                for k, j_ in enumerate(j_range):
                    self[i, j_] = value[0, k]
            else:
                raise MatrixValueError(f'Matrix of size {value.m}×{value.n} does not fit in {len(j_range)} places')

        else:
            for j_ in j_range:
                self[i, j_] = value

    def __setitem_slices(self, i: slice, j: slice, value: N | Sequence[N] | Self) -> None:
        i_range = list(self.__i_range(i))
        j_range = list(self.__j_range(j))

        if isinstance(value, Sequence):
            raise TypeError('Cannot assign a list onto a matrix')

        if isinstance(value, BaseMatrix):
            if value.m == len(i_range) and value.n == len(j_range):
                for i_ in i_range:
                    for j_ in j_range:
                        self[i_, j_] = value[i_, j_]
            else:
                raise MatrixValueError(f'Matrix of size {value.m}×{value.n} does not fit in {len(i_range)}×{len(j_range)} places')

        else:
            for i_ in i_range:
                for j_ in j_range:
                    self[i_, j_] = value

    @overload
    def __setitem__(self, key: tuple[int, int], value: N) -> None: ...
    @overload
    def __setitem__(self, key: tuple[int, slice], value: N | Sequence[N] | Self) -> None: ...
    @overload
    def __setitem__(self, key: tuple[slice, int], value: N | Sequence[N] | Self) -> None: ...
    @overload
    def __setitem__(self, key: tuple[slice, slice], value: N | Self) -> None: ...
    def __setitem__(self, key: tuple[int | slice, int | slice], value: N | Sequence[N] | Self) -> None:
        match key:
            case slice(), slice():
                self.__setitem_slices(*key, value)
            case slice(), int():
                self.__setitem_islice(*key, value)
            case int(), slice():
                self.__setitem_jslice(*key, value)
            case int(), int():
                i, j = key

                if i >= self.m or i < -self.m:
                    raise MatrixIndexError(f'Attempted to access row with index {i}, but the matrix has only {self.m} rows')

                if j >= self.n or j < -self.n:
                    raise MatrixIndexError(f'Attempted to access column with index {j}, but the matrix has only {self.n} columns')

                self.payload[linearize_index(self.dimensions, key)] = cast(N, value)

    def get_rows(self) -> Sequence[Sequence[N]]:
        return [
            list(self[i, :])
            for i in range(self.m)
        ]

    def get_cols(self) -> Sequence[Sequence[N]]:
        return [
            list(self[:, j])
            for j in range(self.n)
        ]

    def is_square(self) -> bool:
        return self.m == self.n

    def transpose(self) -> Self:
        return self.from_factory(
            self.n,
            self.m,
            lambda i, j: self[j, i]
        )

    def stringify_value(self, value: N) -> str:
        return str(value)

    # These two methods are useful for pytest's approx function
    def __iter__(self) -> Iterator[N]:
        return iter(self.payload)

    def __len__(self) -> int:
        return len(self.payload)

    @string_accumulator()
    def __str__(self) -> Iterable[str]:  # noqa: PLE0307
        if self.m == 0 or self.n == 0:
            yield f'({self.m}×{self.n} matrix)\n'

        items = [
            [self.stringify_value(value) for value in row]
            for row in self.get_rows()
        ]

        col_widths = [
            max(len(items[i][j]) for i in range(self.m))
            for j in range(self.n)
        ]

        for i, row in enumerate(items):
            if self.m == 1:
                yield SpecialChars.single_left
            elif i == 0:
                yield SpecialChars.upper_left
            elif i == self.m - 1:
                yield SpecialChars.lower_left
            else:
                yield SpecialChars.pipe

            yield ' '

            for j, (value, width) in enumerate(zip(row, col_widths, strict=True)):
                yield value.ljust(width + (2 if j < len(row) - 1 else 0))

            yield ' '

            if self.n == 1:
                yield SpecialChars.single_right
            elif i == 0:
                yield SpecialChars.upper_right
            elif i == self.m - 1:
                yield SpecialChars.lower_right
            else:
                yield SpecialChars.pipe

            yield '\n'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseMatrix):
            return NotImplemented

        return self.payload == other.payload

    def __add__(self, other: Self) -> Self:
        if self.m != other.m or self.n != other.n:
            return NotImplemented

        return self.from_factory(
            self.m,
            self.n,
            lambda i, j: self[i, j] + other[i, j]
        )

    def __rmul__(self, c: N) -> Self:
        return self.from_factory(
            self.m,
            self.n,
            lambda i, j: c * self[i, j]
        )

    def __matmul__(self, other: Self) -> Self:
        if self.n != other.m:
            return NotImplemented

        return self.from_factory(
            self.m,
            self.n,
            # We avoid using sum since it starts at zero, perplexing tropical arithmetic
            lambda i, j: functools.reduce(operator.add, (x * y for x, y in zip(self[i, :], other[:, j], strict=True)))
        )


class MatrixSubtractionMixin[N: IRing](BaseMatrix[N]):
    def __neg__(self) -> Self:
        return self.lift_to_scalar(-1) * self

    def __sub__(self, other: Self) -> Self:
        if self.m != other.m or self.n != other.n:
            return NotImplemented

        return self + (-other)


class MatrixDivisionMixin[N: IField](BaseMatrix[N]):
    def __truediv__(self, other: N) -> Self:
        return (self.lift_to_scalar(1) / other) * self
