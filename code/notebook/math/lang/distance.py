from ..linalg.matrix import zeros


def hamming(v: str, w: str) -> int:
    assert len(v) == len(w)
    return sum(a != b for a, b in zip(v, w, strict=True))


# This is alg:wagner_fisher in the monograph
def wagner_fisher(v: str, w: str) -> int:
    mtx = zeros(len(v) + 1, len(w) + 1)

    for i in range(len(v) + 1):
        mtx[(i, 0)] = i

    for j in range(len(w) + 1):
        mtx[(0, j)] = j

    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            mtx[(i, j)] = min(
                mtx[(i - 1, j)] + 1,
                mtx[(i, j - 1)] + 1,
                mtx[(i - 1, j - 1)] + (0 if v[i - 1] == w[j - 1] else 1)
            )

    return mtx[(len(v), len(w))]
