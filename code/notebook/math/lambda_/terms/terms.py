from typing import NamedTuple

from ....parsing.identifiers import LatinIdentifier
from ..alphabet import TermConnective


class Constant(NamedTuple):
    name: str

    def __str__(self) -> str:
        return str(self.name)


class Variable(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class Application(NamedTuple):
    a: 'Term'
    b: 'Term'

    def __str__(self) -> str:
        return f'({self.a}{self.b})'


class Abstraction(NamedTuple):
    var: Variable
    sub: 'Term'

    def __str__(self) -> str:
        return f'({TermConnective.l}{self.var}.{self.sub})'


Term = Constant | Variable | Application | Abstraction
