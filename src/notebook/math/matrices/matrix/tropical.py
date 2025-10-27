from typing import Self

from ...rings.tropical import MaxPlusFloat, MinPlusFloat
from .common import ISemiringMatrix
from .float import FloatMatrix


class MinPlusMatrix(ISemiringMatrix[MinPlusFloat], semiring=MinPlusFloat):
    @classmethod
    def from_float_matrix(cls, mat: FloatMatrix) -> Self:
        return cls.from_factory(
            mat.m,
            mat.n,
            lambda i, j: MinPlusFloat(mat[i, j])
        )


class MaxPlusMatrix(ISemiringMatrix[MaxPlusFloat], semiring=MaxPlusFloat):
    @classmethod
    def from_float_matrix(cls, mat: FloatMatrix) -> Self:
        return cls.from_factory(
            mat.m,
            mat.n,
            lambda i, j: MaxPlusFloat(mat[i, j])
        )
