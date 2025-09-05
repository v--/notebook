from typing import override

from .common import INormedFieldMatrix
from .int import IntMatrix


class FloatMatrix(INormedFieldMatrix[float], semiring=float):
    @override
    def stringify_value(self, value: float) -> str:
        return f'{value:.3f}'

    def round(self) -> IntMatrix:
        return IntMatrix(
            self.n, self.m,
            lambda i, j: round(self[i, j])
        )
