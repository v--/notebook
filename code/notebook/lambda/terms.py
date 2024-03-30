from typing import NamedTuple


class Variable(NamedTuple):
    name: str

    def __str__(self):
        return self.name


class Application(NamedTuple):
    a: 'Term'
    b: 'Term'

    def __str__(self):
        return f'({self.a}{self.b})'


class Abstraction(NamedTuple):
    var: Variable
    sub: 'Term'

    def __str__(self):
        return f'(λ{self.var}.{self.sub})'


Term = Variable | Application | Abstraction
