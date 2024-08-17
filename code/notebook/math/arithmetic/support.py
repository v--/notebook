from typing import Literal


SignT = Literal[-1, 0, 1]


def sgn(x: float) -> SignT:
    if x == 0:
        return 0

    if x > 0:
        return 1

    return -1
