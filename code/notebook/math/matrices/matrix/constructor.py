from typing import Self

from ...rings.arithmetic import ISemiring
from .base import BaseMatrix


class MatrixConstructorMixin[N: ISemiring](BaseMatrix[N]):
    @classmethod
    def fill(cls, n: int, m: int | None = None, *, value: N) -> Self:
        if m is None:
            m = n

        if n == 0 or m == 0:
            return cls(n, m)

        return cls.from_rows([
            [value for j in range(n)]
            for i in range(m)
        ])

    @classmethod
    def zeros(cls, n: int, m: int | None = None) -> Self:
        return cls.fill(n, m, value=cls.lift(0))

    @classmethod
    def ones(cls, n: int, m: int | None = None) -> Self:
        return cls.fill(n, m, value=cls.lift(1))

    @classmethod
    def eye(cls, n: int, m: int | None = None) -> Self:
        result = cls.zeros(n, m)

        for i in range(min(n, m) if m is not None else n):
            result[i, i] = cls.lift(1)

        return result
