from textwrap import dedent

import pytest

from ..exceptions import MatrixIndexError, MatrixValueError
from .float import FloatMatrix
from .int import IntMatrix


class TestMatrixToStr:
    def test_zero(self) -> None:
        assert str(IntMatrix.eye(0)) == '(0×0 matrix)\n'

    def test_one_by_one(self) -> None:
        assert str(IntMatrix.eye(1)) == dedent('''\
            ( 1 )
        ''')

    def test_123(self, mat123: IntMatrix) -> None:
        assert str(mat123) == dedent('''\
            ⎛ 1  2  3  ⎞
            ⎜ 4  5  6  ⎜
            ⎝ 7  8  10 ⎠
        ''')


class TestMatrixGetter:
    def test_single_success(self, mat123: IntMatrix) -> None:
        assert mat123[0, 0] == 1
        assert mat123[1, 1] == 5
        assert mat123[2, 2] == 10

    def test_single_failure_out_of_bounds(self, mat123: IntMatrix) -> None:
        # Row index too large
        with pytest.raises(MatrixIndexError):
            mat123[3, 2]

    def test_single_success_negative(self, mat123: IntMatrix) -> None:
        assert mat123[-1, -1] == 10
        assert mat123[-2, -2] == 5
        assert mat123[-3, -3] == 1

    def test_single_failure_negative_out_of_bounds(self, mat123: IntMatrix) -> None:
        # Row index too small
        with pytest.raises(MatrixIndexError):
            mat123[-4, 2]

    def test_col_range_success(self, mat123: IntMatrix) -> None:
        assert mat123[0, :] == IntMatrix.from_rows([[1, 2, 3]])

    def test_row_range_success(self, mat123: IntMatrix) -> None:
        assert mat123[:, 0] == IntMatrix.from_rows([[1], [4], [7]])

    def test_col_range_failure(self, mat123: IntMatrix) -> None:
        # Column slice has out-of-bound indices
        with pytest.raises(MatrixIndexError):
            mat123[0, 1:4]

    def test_double_range_success(self, mat123: IntMatrix) -> None:
        assert mat123[:, :] == mat123


class TestMatrixSetter:
    def test_single(self, mat123: IntMatrix) -> None:
        mat123[1, 1] = 10
        assert mat123[1, 1] == 10

    def test_range_single(self, mat123: IntMatrix) -> None:
        mat123[1, :] = -1
        assert mat123[1, 0] == -1
        assert mat123[1, 1] == -1
        assert mat123[1, 2] == -1

    def test_range_multiple_success(self, mat123: IntMatrix) -> None:
        mat123[1, :] = [-1] * 3
        assert mat123[1, 0] == -1
        assert mat123[1, 1] == -1
        assert mat123[1, 2] == -1

    def test_range_multiple_success_manual_range(self, mat123: IntMatrix) -> None:
        mat123[1, 1:3] = [-1] * 2
        assert mat123[1, 0] == 4
        assert mat123[1, 1] == -1
        assert mat123[1, 2] == -1

    def test_range_multiple_failure_manual_range(self, mat123: IntMatrix) -> None:
        # Column slice has out-of-bound indices
        with pytest.raises(MatrixIndexError):
            mat123[1, 1:4] = [-1] * 3

    def test_range_multiple_failure_auto_range(self, mat123: IntMatrix) -> None:
        # List too large
        with pytest.raises(MatrixValueError, match='List of length 4 does not fit in 3 places'):
            mat123[1, :] = [-1] * 4

    def test_all_success(self, mat123: IntMatrix) -> None:
        mat123[:, :] = IntMatrix.eye(3)
        assert mat123 == IntMatrix.eye(3)

    def test_all_failure(self, mat123: IntMatrix) -> None:
        # IntMatrix of incompatible size
        with pytest.raises(MatrixValueError, match='Matrix of size 2×2 does not fit in 3×3 places'):
            mat123[:, :] = IntMatrix.eye(2)


class TestMatrixAddition:
    def test_simple_addition(self, mat123: IntMatrix, lower_pascal3: IntMatrix) -> None:
        res = mat123 + lower_pascal3
        assert res[0, 0] == 2
        assert res[1, 1] == 6
        assert res[2, 2] == 11

    def test_associativity(self, mat123: IntMatrix, lower_pascal3: IntMatrix) -> None:
        assert (IntMatrix.eye(3) + mat123) + lower_pascal3 == IntMatrix.eye(3) + (mat123 + lower_pascal3)

    def test_commutativity(self, mat123: IntMatrix) -> None:
        assert IntMatrix.eye(3) + mat123 == mat123 + IntMatrix.eye(3)

    def test_neutral_element(self, mat123: IntMatrix) -> None:
        assert mat123 == IntMatrix.zeros(3) + mat123

    def test_inverse(self, mat123: IntMatrix) -> None:
        assert -mat123 + mat123 == IntMatrix.zeros(3)


class TestMatrixMultiplication:
    def test_simple_multiplication(self, mat123: IntMatrix, lower_pascal3: IntMatrix) -> None:
        res = mat123 @ lower_pascal3
        assert res[0, 0] == 6
        assert res[1, 1] == 17
        assert res[2, 2] == 10

    def test_associativity(self, mat123: IntMatrix, lower_pascal3: IntMatrix) -> None:
        assert (IntMatrix.eye(3) @ mat123) @ lower_pascal3 == IntMatrix.eye(3) @ (mat123 @ lower_pascal3)

    def test_commutativity(self, mat123: IntMatrix) -> None:
        assert IntMatrix.eye(3) @ mat123 == mat123 @ IntMatrix.eye(3)

    def test_neutral_element(self, mat123: IntMatrix) -> None:
        assert mat123 == IntMatrix.eye(3) @ mat123

    def test_inverse(self, mat123: IntMatrix, mat123inv: FloatMatrix) -> None:
        assert mat123inv @ FloatMatrix.lift_matrix(mat123) == pytest.approx(FloatMatrix.eye(3))
