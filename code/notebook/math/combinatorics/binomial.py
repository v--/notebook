from ..linalg.matrix import Matrix, zeros


def choose(n: int, k: int) -> int:
    if k > n:
        return 0

    if k == 0 or k == n:
        return 1

    return choose(n - 1, k) + choose(n - 1, k - 1)


# This is def:pascal_matrix/lower in the monograph
def pascals_lower_matrix(n: int) -> Matrix[int]:
    matrix = zeros(n)

    for i in range(n):
        matrix[i, 0] = 1
        matrix[i, i] = 1

    for i in range(1, n):
        for j in range(1, i):
            matrix[i, j] = matrix[i - 1, j] + matrix[i - 1, j - 1]

    return matrix


# This is def:pascal_matrix/upper in the monograph
def pascals_upper_matrix(n: int) -> Matrix[int]:
    return pascals_lower_matrix(n).transpose()


# This is def:pascal_matrix/symmetric in the monograph
def pascals_symmetric_matrix(n: int) -> Matrix[int]:
    matrix = zeros(n)

    for i in range(n):
        matrix[i, 0] = 1

    for j in range(n):
        matrix[0, j] = 1

    for i in range(1, n):
        for j in range(1, n):
            matrix[i, j] = matrix[i - 1, j] + matrix[i, j - 1]

    return matrix
