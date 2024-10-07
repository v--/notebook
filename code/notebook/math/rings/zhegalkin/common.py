from .polynomial import ZhegalkinPolynomial


T = ZhegalkinPolynomial(payload=[], free=True)
F = ZhegalkinPolynomial(payload=[], free=False)

x = ZhegalkinPolynomial(payload=[frozenset('x')], free=False)
y = ZhegalkinPolynomial(payload=[frozenset('y')], free=False)
