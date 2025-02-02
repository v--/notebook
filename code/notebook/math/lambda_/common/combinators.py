from ..parsing import parse_pure_term
from ..terms import UntypedAbstraction, UntypedApplication, UntypedTerm
from .variables import x


i = parse_pure_term('(λx.x)')
k = parse_pure_term('(λx.(λy.x))')
s = parse_pure_term('(λx.(λy.(λz.((xz)(yz)))))')
y = parse_pure_term('(λf.((λx.(f(xx)))(λx.(f(xx)))))')


def get_omega(n: int) -> UntypedTerm:
    assert n >= 1

    content: UntypedTerm = x

    for _ in range(1, n):
        content = UntypedApplication(content, x)

    return UntypedAbstraction(x, content)


omega2 = get_omega(2)
omega3 = get_omega(3)
big_omega = UntypedApplication(omega2, omega2)
