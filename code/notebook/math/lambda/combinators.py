from .parsing import parse_term
from .terms import Abstraction, Application, LambdaTerm
from .variables import common as var


i = parse_term('(λx.x)')
k = parse_term('(λx.(λy.x))')
s = parse_term('(λx.(λy.(λz.((xz)(yz)))))')
y = parse_term('(λf.((λx.(f(xx)))(λx.(f(xx)))))')


def get_omega(n: int) -> LambdaTerm:
    assert n >= 1

    content: LambdaTerm = var.x

    for _ in range(1, n):
        content = Application(content, var.x)

    return Abstraction(var.x, content)


omega2 = get_omega(2)
omega3 = get_omega(3)
big_omega = Application(omega2, omega2)
