import pytest

from .matrix import Matrix


@pytest.fixture()
def mat123() -> Matrix[int]:
    return Matrix([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 10]
    ])


@pytest.fixture()
def mat123inv() -> Matrix[float]:
    return Matrix([
        [-2 / 3, -4 / 3,   1],
        [-2 / 3,  11 / 3, -2],
        [1,      -2,       1]
    ])


@pytest.fixture()
def lower_pascal3() -> Matrix[int]:
    return Matrix([
        [1, 0, 0],
        [1, 1, 0],
        [1, 2, 1]
    ])
