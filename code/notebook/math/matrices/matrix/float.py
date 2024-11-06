from typing import override

from .common import INormedFieldMatrix


class FloatMatrix(INormedFieldMatrix[float], semiring=float):
    @override
    def stringify_value(self, value: float) -> str:
        return f'{value:.3f}'
