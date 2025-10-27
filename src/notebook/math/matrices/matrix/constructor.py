from collections.abc import Sequence
from typing import Self

from ...rings.types import ISemiring
from ..exceptions import MatrixIndexError
from .base import BaseMatrix


class MatrixConstructorMixin[N: ISemiring](BaseMatrix[N]):
    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[N]]) -> Self:
        if len(rows) == 0:
            raise MatrixIndexError('Cannot determine matrix dimensions from empty list')

        m = len(rows)
        n = len(rows[0])

        for i, row in enumerate(rows):
            if len(row) != n:
                raise MatrixIndexError(f'Row with index {i} has {len(row)} elements, but first row has {m} elements')

        return cls.from_factory(m, n, lambda i, j: rows[i][j])

    @classmethod
    def lift_matrix(cls, mat: BaseMatrix[int]) -> Self:
        return cls.from_factory(
            mat.m,
            mat.n,
            lambda i, j: cls.lift_to_scalar(mat[i, j])
        )

    @classmethod
    def fill(cls, m: int, n: int | None = None, *, value: N) -> Self:
        if n is None:
            n = m

        return cls.from_factory(m, n, lambda i, j: value)  # noqa: ARG005

    @classmethod
    def zeros(cls, m: int, n: int | None = None) -> Self:
        return cls.fill(m, n, value=cls.lift_to_scalar(0))

    @classmethod
    def ones(cls, m: int, n: int | None = None) -> Self:
        return cls.fill(m, n, value=cls.lift_to_scalar(1))

    @classmethod
    def eye(cls, m: int, n: int | None = None) -> Self:
        if n is None:
            n = m

        return cls.from_factory(n, m, lambda i, j: cls.lift_to_scalar(int(i == j)))
