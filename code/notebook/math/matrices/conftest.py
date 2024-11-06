import pytest

from .matrix import FloatMatrix, IntMatrix


@pytest.fixture
def mat123() -> IntMatrix:
    return IntMatrix.from_rows([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 10]
    ])


@pytest.fixture
def mat123f(mat123: IntMatrix) -> FloatMatrix:
    return FloatMatrix.from_int_matrix(mat123)


@pytest.fixture
def mat123inv() -> FloatMatrix:
    return FloatMatrix.from_rows([
        [-2 / 3, -4 / 3,   1],
        [-2 / 3,  11 / 3, -2],
        [1,      -2,       1]
    ])


@pytest.fixture
def lower_pascal3() -> IntMatrix:
    return IntMatrix.from_rows([
        [1, 0, 0],
        [1, 1, 0],
        [1, 2, 1]
    ])


@pytest.fixture
def lower_pascal3f(lower_pascal3: IntMatrix) -> FloatMatrix:
    return FloatMatrix.from_int_matrix(lower_pascal3)
