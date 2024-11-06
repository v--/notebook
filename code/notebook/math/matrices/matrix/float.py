from .common import INormedFieldMatrix


class FloatMatrix(INormedFieldMatrix[float], semiring=float):
    def stringify_value(self, value: float) -> str:
        return f'{value:.3f}'
