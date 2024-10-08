import pytest

from .matrix import Matrix, eye, is_close, linearize_index, zeros


def test_linearize_index() -> None:
    assert linearize_index(dimensions=[], indices=[]) == 0
    assert linearize_index(dimensions=[10], indices=[5]) == 5
    assert linearize_index(dimensions=[10, 5], indices=[5, 3]) == 28
    assert linearize_index(dimensions=[10, 5, 9], indices=[5, 3, 8]) == 260


def test_matrix_getter(mat123: Matrix[int]) -> None:
    assert mat123[0, 0] == 1
    assert mat123[1, 1] == 5
    assert mat123[2, 2] == 10

    # Row index too large
    with pytest.raises(IndexError):
        mat123[3, 2]

    assert mat123[-1, -1] == 10
    assert mat123[-2, -2] == 5
    assert mat123[-3, -3] == 1

    # Row index too small
    with pytest.raises(IndexError):
        mat123[-4, 2]

    assert mat123[0, :] == Matrix([[1, 2, 3]])
    assert mat123[:, 0] == Matrix([[1], [4], [7]])

    # Column slice has out-of-bound indices
    with pytest.raises(IndexError):
        mat123[0, 1:4]

    assert mat123[:, :] == mat123


def test_matrix_setter(mat123: Matrix[int]) -> None:
    mod = mat123[:, :]
    mod[1, 1] = 10
    assert mod[1, 1] == 10

    mod[1, :] = -1
    assert mod[1, 0] == -1
    assert mod[1, 1] == -1
    assert mod[1, 2] == -1

    mod[1, :] = [-1] * 3
    assert mod[1, 0] == -1
    assert mod[1, 1] == -1
    assert mod[1, 2] == -1

    # Column slice has out-of-bound indices
    with pytest.raises(IndexError):
        mod[1, 1:4] = [-1] * 3

    # List too large
    with pytest.raises(ValueError, match='List of length 4 does not fit in 3 places'):
        mod[1, :] = [-1] * 4

    mod[:, :] = eye(3)
    assert mod == eye(3)

    # Matrix of incompatible size
    with pytest.raises(ValueError, match='Matrix of size 2×2 does not fit in 3×3 places'):
        mod[:, :] = eye(2)


def test_matrix_addition(mat123: Matrix[int], lower_pascal3: Matrix[int]) -> None:
    res = mat123 + lower_pascal3
    assert res[0, 0] == 2
    assert res[1, 1] == 6
    assert res[2, 2] == 11


def test_matrix_addition_properties(mat123: Matrix[int], lower_pascal3: Matrix[int]) -> None:
    # Associativity
    assert (eye(3) + mat123) + lower_pascal3 == eye(3) + (mat123 + lower_pascal3)

    # Commutativity
    assert eye(3) + mat123 == mat123 + eye(3)

    # Identity element
    assert mat123 == zeros(3) + mat123

    # Negative element
    assert -mat123 + mat123 == zeros(3)


def test_matrix_mult(mat123: Matrix[int], lower_pascal3: Matrix[int]) -> None:
    res = mat123 @ lower_pascal3
    assert res[0, 0] == 6
    assert res[1, 1] == 17
    assert res[2, 2] == 10


def test_matrix_mult_properties(mat123: Matrix[int], mat123inv: Matrix[float], lower_pascal3: Matrix[int]) -> None:
    # Associativity
    assert is_close((eye(3) @ mat123) @ lower_pascal3, eye(3) @ (mat123 @ lower_pascal3))

    # Commutativity
    assert is_close(eye(3) @ mat123, mat123 @ eye(3))

    # Identity element
    assert is_close(mat123, eye(3) @ mat123)

    # Negative element
    assert is_close(mat123inv @ mat123, eye(3))
