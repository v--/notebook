from typing import NamedTuple


class Variable(NamedTuple):
    name: str

    def __str__(self) -> str:
        return self.name


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
