from typing import Self

from ...rings.tropical import MaxPlusFloat, MinPlusFloat
from .common import ISemiringMatrix
from .float import FloatMatrix


class MinPlusMatrix(ISemiringMatrix[MinPlusFloat], semiring=MinPlusFloat):
    @classmethod
    def from_float_matrix(cls, mat: FloatMatrix) -> Self:
        return cls.from_rows([
            [MinPlusFloat(value) for value in row]
            for row in mat.get_rows()
        ])


class MaxPlusMatrix(ISemiringMatrix[MaxPlusFloat], semiring=MaxPlusFloat):
    @classmethod
    def from_float_matrix(cls, mat: FloatMatrix) -> Self:
        return cls.from_rows([
            [MaxPlusFloat(value) for value in row]
            for row in mat.get_rows()
        ])
