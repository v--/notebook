from .matrix import INormedFieldMatrix


def max_norm[M: INormedFieldMatrix](mat: M) -> float:
    return max(
        abs(value)
        for row in mat.get_rows()
        for value in row
    )


def are_close[M: INormedFieldMatrix](a: M, b: M, *, tolerance: float = 1e-6) -> bool:
    return a.n == b.n and a.m == b.m and max_norm(b - a) < tolerance


def is_unit[M: INormedFieldMatrix](mat: M, *, tolerance: float = 1e-6) -> bool:
    return mat.is_square() and are_close(mat, mat.eye(mat.n), tolerance=tolerance)
