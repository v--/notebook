from typing import NamedTuple

from ....parsing.identifiers import LatinIdentifier
from ..alphabet import TermConnective
from ..types import SimpleTypeSchema
from .terms import Constant


class VariablePlaceholder(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class TermPlaceholder(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class ApplicationSchema(NamedTuple):
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


class AbstractionSchema(NamedTuple):
    var: VariablePlaceholder
    sub: 'TermSchema'
    var_type: SimpleTypeSchema | None

    def __str__(self) -> str:
        return f'({TermConnective.l}{self.var}.{self.sub})'


class UntypedAbstractionSchema(AbstractionSchema):
    sub: 'UntypedTermSchema'
    var_type: None


class TypedAbstractionSchema(AbstractionSchema):
    sub: 'TypedTermSchema'
    var_type: SimpleTypeSchema


TermSchema = Constant | VariablePlaceholder | TermPlaceholder | ApplicationSchema | AbstractionSchema
UntypedTermSchema = Constant | VariablePlaceholder | TermPlaceholder | UntypedApplicationSchema | UntypedAbstractionSchema
TypedTermSchema = Constant | VariablePlaceholder | TermPlaceholder | TypedApplicationSchema | TypedAbstractionSchema
