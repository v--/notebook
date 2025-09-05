from ..exceptions import LambdaCalculusError
from ..parsing import parse_untyped_term
from ..terms import UntypedAbstraction, UntypedApplication, UntypedTerm
from .variables import x, y


def church_numeral(n: int) -> UntypedAbstraction:
    assert n >= 0

    content: UntypedTerm = y

    for _ in range(n):
        content = UntypedAbstraction(x, content)

    return UntypedAbstraction(x, UntypedAbstraction(y, content))


def church_numeral_to_int(term: UntypedAbstraction) -> int:
    if not isinstance(term.body, UntypedAbstraction):
        raise LambdaCalculusError(f'Invalid Church numeral {term}')

    current = term.body.body
    n = 0

    while isinstance(current, UntypedApplication) and current.left == term.var:
        n += 1
        current = current.right

    if current == term.body.var:
        return n

    raise LambdaCalculusError(f'Invalid Church numeral {term}')


succ = parse_untyped_term('(λf.(λx.(λy.(x((fx)y)))))')
