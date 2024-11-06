from .tropical import MinPlusMatrix


def test_matrix_add(n: int = 3) -> None:
    eye = MinPlusMatrix.eye(n)
    assert eye + eye == eye


def test_matrix_mul(n: int = 3) -> None:
    eye = MinPlusMatrix.eye(n)
    assert eye @ eye == eye
