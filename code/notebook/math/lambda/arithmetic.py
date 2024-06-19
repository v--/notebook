from .exceptions import LambdaError
from .parsing import parse_term
from .terms import Abstraction, Application, LambdaTerm
from .variables import common as var


def church_numeral(n: int) -> LambdaTerm:
    assert n >= 0

    content: LambdaTerm = var.y

    for _ in range(n):
        content = Abstraction(var.x, content)

    return Abstraction(var.x, Abstraction(var.y, content))


def church_numeral_to_int(term: LambdaTerm) -> int:
    assert isinstance(term, Abstraction)
    assert isinstance(term.sub, Abstraction)

    current = term.sub.sub
    n = 0

    while isinstance(current, Application) and current.a == term.var:
        n += 1
        current = current.b

    if current == term.sub.var:
        return n

    raise LambdaError(f'Invalid Church numeral {term}')


succ = parse_term('(λf.(λx.(λy.(x((fx)y)))))')
