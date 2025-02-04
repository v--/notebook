from dataclasses import dataclass

from ....parsing.identifiers import LatinIdentifier
from ..alphabet import TermConnective
from ..types import SimpleType


@dataclass(frozen=True)
class Constant:
    name: str

    def __str__(self) -> str:
        return str(self.name)


@dataclass(frozen=True)
class Variable:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class Application:
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


@dataclass(frozen=True)
class Abstraction:
    var: Variable
    sub: 'Term'
    var_type: SimpleType | None = None

    def __str__(self) -> str:
        if self.var_type is None:
            return f'({TermConnective.l}{self.var}.{self.sub})'

        return f'({TermConnective.l}{self.var}:{self.var_type}.{self.sub})'


class UntypedAbstraction(Abstraction):
    sub: 'UntypedTerm'
    var_type: None


class TypedAbstraction(Abstraction):
    sub: 'TypedTerm'
    var_type: SimpleType


Term = Constant | Variable | Application | Abstraction
UntypedTerm = Constant | Variable | UntypedApplication | UntypedAbstraction
TypedTerm = Constant | Variable | TypedApplication | TypedAbstraction
