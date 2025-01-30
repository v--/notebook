from ..exceptions import LambdaCalculusError
from ..parsing import parse_pure_term
from ..terms import Abstraction, Application, Term
from .variables import x, y


def church_numeral(n: int) -> Term:
    assert n >= 0

    content: Term = y

    for _ in range(n):
        content = Abstraction(x, content)

    return Abstraction(x, Abstraction(y, content))


def church_numeral_to_int(term: Term) -> int:
    assert isinstance(term, Abstraction)
    assert isinstance(term.sub, Abstraction)

    current = term.sub.sub
    n = 0

    while isinstance(current, Application) and current.a == term.var:
        n += 1
        current = current.b

    if current == term.sub.var:
        return n

    raise LambdaCalculusError(f'Invalid Church numeral {term}')


succ = parse_pure_term('(λf.(λx.(λy.(x((fx)y)))))')
