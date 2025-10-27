import math


# This is eq:thm:stirlings_gamma_approximation/mu in the monograph
def stirling_mu(x: float, terms: int) -> float:
    return sum(
        (x + k + 1 / 2) * math.log(1 + 1 / (x + k)) - 1
        for k in range(terms)
    )


# This is eq:thm:stirlings_gamma_approximation in the monograph
def stirling(x: float) -> float:
    assert x > 0
    return math.sqrt(2 * math.pi) * x ** (x - 1 / 2) * math.exp(-x)
