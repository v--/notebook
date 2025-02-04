from dataclasses import dataclass

from ....parsing.identifiers import LatinIdentifier
from ..alphabet import TermConnective
from ..types import SimpleTypeSchema
from .terms import Constant


@dataclass(frozen=True)
class VariablePlaceholder:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class TermPlaceholder:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class ApplicationSchema:
    a: 'TermSchema'
    b: 'TermSchema'

    def __str__(self) -> str:
        return f'({self.a}{self.b})'


class UntypedApplicationSchema(ApplicationSchema):
    a: 'UntypedTermSchema'
    b: 'UntypedTermSchema'


class TypedApplicationSchema(ApplicationSchema):
    a: 'TypedTermSchema'
    b: 'TypedTermSchema'


@dataclass(frozen=True)
class AbstractionSchema:
    var: VariablePlaceholder
    sub: 'TermSchema'
    var_type: SimpleTypeSchema | None = None

    def __str__(self) -> str:
        if self.var_type is None:
            return f'({TermConnective.l}{self.var}.{self.sub})'

        return f'({TermConnective.l}{self.var}:{self.var_type}.{self.sub})'


class UntypedAbstractionSchema(AbstractionSchema):
    sub: 'UntypedTermSchema'
    var_type: None


class TypedAbstractionSchema(AbstractionSchema):
    sub: 'TypedTermSchema'
    var_type: SimpleTypeSchema


TermSchema = Constant | VariablePlaceholder | TermPlaceholder | ApplicationSchema | AbstractionSchema
UntypedTermSchema = Constant | VariablePlaceholder | TermPlaceholder | UntypedApplicationSchema | UntypedAbstractionSchema
TypedTermSchema = Constant | VariablePlaceholder | TermPlaceholder | TypedApplicationSchema | TypedAbstractionSchema
