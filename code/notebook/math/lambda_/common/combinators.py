from ..parsing import parse_pure_term
from ..terms import Abstraction, Application, Term
from .variables import x


i = parse_pure_term('(λx.x)')
k = parse_pure_term('(λx.(λy.x))')
s = parse_pure_term('(λx.(λy.(λz.((xz)(yz)))))')
y = parse_pure_term('(λf.((λx.(f(xx)))(λx.(f(xx)))))')


def get_omega(n: int) -> Term:
    assert n >= 1

    content: Term = x

    for _ in range(1, n):
        content = Application(content, x)

    return Abstraction(x, content)


omega2 = get_omega(2)
omega3 = get_omega(3)
big_omega = Application(omega2, omega2)
