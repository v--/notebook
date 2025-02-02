from typing import NamedTuple

from ....parsing.identifiers import LatinIdentifier
from ..alphabet import TermConnective
from ..types import SimpleType


class Constant(NamedTuple):
    name: str
    type: SimpleType | None = None

    def __str__(self) -> str:
        return str(self.name)


class PlainConstant(Constant):
    type: None


class AnnotatedConstant(Constant):
    type: SimpleType


class Variable(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class Application(NamedTuple):
    a: 'Term'
    b: 'Term'

    def __str__(self) -> str:
        return f'({self.a}{self.b})'


class UntypedApplication(Application):
    a: 'UntypedTerm'
    b: 'UntypedTerm'


class TypedApplication(Application):
    a: 'TypedTerm'
    b: 'TypedTerm'


class Abstraction(NamedTuple):
    var: Variable
    sub: 'Term'
    var_type: SimpleType | None = None

    def __str__(self) -> str:
        return f'({TermConnective.l}{self.var}.{self.sub})'


class UntypedAbstraction(Abstraction):
    var_type: None
    sub: 'UntypedTerm'


class TypedAbstraction(Abstraction):
    var_type: SimpleType
    sub: 'TypedTerm'


Term = Constant | Variable | Application | Abstraction
UntypedTerm = PlainConstant | Variable | UntypedApplication | UntypedAbstraction
TypedTerm = AnnotatedConstant | Variable | TypedApplication | TypedAbstraction
