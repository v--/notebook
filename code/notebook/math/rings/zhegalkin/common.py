from .polynomial import ZhegalkinPolynomial


T = ZhegalkinPolynomial(payload=frozenset(), free=True)
F = ZhegalkinPolynomial(payload=frozenset(), free=False)

x = ZhegalkinPolynomial(payload=frozenset([frozenset('x')]), free=False)
y = ZhegalkinPolynomial(payload=frozenset([frozenset('y')]), free=False)
