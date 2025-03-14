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
class MixedApplication:
    a: 'MixedTerm'
    b: 'MixedTerm'

    def __str__(self) -> str:
        return f'({self.a}{self.b})'


class UntypedApplication(MixedApplication):
    a: 'UntypedTerm'
    b: 'UntypedTerm'


class TypedApplication(MixedApplication):
    a: 'TypedTerm'
    b: 'TypedTerm'


@dataclass(frozen=True)
class MixedAbstraction:
    var: Variable
    sub: 'MixedTerm'
    var_type: SimpleType | None = None

    def __str__(self) -> str:
        if self.var_type is None:
            return f'({TermConnective.LAMBDA}{self.var}.{self.sub})'

        return f'({TermConnective.LAMBDA}{self.var}:{self.var_type}.{self.sub})'


class UntypedAbstraction(MixedAbstraction):
    sub: 'UntypedTerm'
    var_type: None


class TypedAbstraction(MixedAbstraction):
    sub: 'TypedTerm'
    var_type: SimpleType


MixedTerm = Constant | Variable | MixedApplication | MixedAbstraction
UntypedTerm = Constant | Variable | UntypedApplication | UntypedAbstraction
TypedTerm = Constant | Variable | TypedApplication | TypedAbstraction
