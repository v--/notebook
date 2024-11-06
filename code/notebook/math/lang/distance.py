from ..matrices.matrix import IntMatrix


def hamming(v: str, w: str) -> int:
    assert len(v) == len(w)
    return sum(a != b for a, b in zip(v, w, strict=True))


# This is alg:wagner_fisher in the monograph
def wagner_fisher(v: str, w: str) -> int:
    mat = IntMatrix.zeros(len(v) + 1, len(w) + 1)

    for i in range(len(v) + 1):
        mat[(i, 0)] = i

    for j in range(len(w) + 1):
        mat[(0, j)] = j

    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            mat[(i, j)] = min(
                mat[(i - 1, j)] + 1,
                mat[(i, j - 1)] + 1,
                mat[(i - 1, j - 1)] + (0 if v[i - 1] == w[j - 1] else 1)
            )

    return mat[(len(v), len(w))]
