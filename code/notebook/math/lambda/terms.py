from typing import NamedTuple

from ...parsing.identifiers import LatinIdentifier


class Variable(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class Application(NamedTuple):
    a: 'LambdaTerm'
    b: 'LambdaTerm'

    def __str__(self) -> str:
        return f'({self.a}{self.b})'


class Abstraction(NamedTuple):
    var: Variable
    sub: 'LambdaTerm'

    def __str__(self) -> str:
        return f'(λ{self.var}.{self.sub})'


LambdaTerm = Variable | Application | Abstraction
