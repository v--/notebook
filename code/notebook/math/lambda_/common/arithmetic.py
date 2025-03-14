from ..exceptions import LambdaCalculusError
from ..parsing import parse_pure_term
from ..terms import MixedApplication, UntypedAbstraction, UntypedTerm
from .variables import x, y


def church_numeral(n: int) -> UntypedTerm:
    assert n >= 0

    content: UntypedTerm = y

    for _ in range(n):
        content = UntypedAbstraction(x, content)

    return UntypedAbstraction(x, UntypedAbstraction(y, content))


def church_numeral_to_int(term: UntypedTerm) -> int:
    assert isinstance(term, UntypedAbstraction)
    assert isinstance(term.sub, UntypedAbstraction)

    current = term.sub.sub
    n = 0

    while isinstance(current, MixedApplication) and current.a == term.var:
        n += 1
        current = current.b

    if current == term.sub.var:
        return n

    raise LambdaCalculusError(f'Invalid Church numeral {term}')


succ = parse_pure_term('(λf.(λx.(λy.(x((fx)y)))))')
