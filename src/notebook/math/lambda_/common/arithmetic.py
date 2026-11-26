from notebook.math.lambda_.exceptions import LambdaCalculusError
from notebook.math.lambda_.parsing import parse_untyped_term
from notebook.math.lambda_.terms import UntypedAbstraction, UntypedApplication, UntypedTerm

from .variables import x, y


def int_to_church_numeral(n: int) -> UntypedAbstraction:
    if n < 0:
        raise LambdaCalculusError(f'Expected a nonnegative integer, but got {n}')

    content: UntypedTerm = y

    for _ in range(n):
        content = UntypedAbstraction(x, content)

    return UntypedAbstraction(x, UntypedAbstraction(y, content))


def church_numeral_to_int(term: UntypedAbstraction) -> int:
    if not isinstance(term.body, UntypedAbstraction):
        raise LambdaCalculusError(f'Invalid Church numeral {term}')

    current = term.body.body
    n = -1

    while isinstance(current, UntypedApplication) and current.left == term.var:
        n += 1
        current = current.right

    if current == term.body.var:
        return n

    raise LambdaCalculusError(f'Invalid Church numeral {term}')


succ = parse_untyped_term('(λn.(λx.(λy.(x((nx)y)))))')
is_even = parse_untyped_term('(λn.((n(λb.(λt.(λf.((bf)t)))))(λx.(λy.y))))')
