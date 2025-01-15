from typing import NamedTuple

from ...parsing.identifiers import LatinIdentifier
from .alphabet import LambdaTermConnective


class Constant(NamedTuple):
    name: str

    def __str__(self) -> str:
        return str(self.name)


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
        return f'({LambdaTermConnective.l}{self.var}.{self.sub})'


LambdaTerm = Constant | Variable | Application | Abstraction


class VariablePlaceholder(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class LambdaTermPlaceholder(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class ApplicationSchema(NamedTuple):
    a: 'LambdaTermSchema'
    b: 'LambdaTermSchema'

    def __str__(self) -> str:
        return f'({self.a}{self.b})'


class AbstractionSchema(NamedTuple):
    var: VariablePlaceholder
    sub: 'LambdaTermSchema'

    def __str__(self) -> str:
        return f'({LambdaTermConnective.l}{self.var}.{self.sub})'


LambdaTermSchema = Constant | VariablePlaceholder | LambdaTermPlaceholder | ApplicationSchema | AbstractionSchema
