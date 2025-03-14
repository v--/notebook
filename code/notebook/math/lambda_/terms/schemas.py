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
class MixedApplicationSchema:
    a: 'MixedTermSchema'
    b: 'MixedTermSchema'

    def __str__(self) -> str:
        return f'({self.a}{self.b})'


class UntypedApplicationSchema(MixedApplicationSchema):
    a: 'UntypedTermSchema'
    b: 'UntypedTermSchema'


class TypedApplicationSchema(MixedApplicationSchema):
    a: 'TypedTermSchema'
    b: 'TypedTermSchema'


@dataclass(frozen=True)
class MixedAbstractionSchema:
    var: VariablePlaceholder
    sub: 'MixedTermSchema'
    var_type: SimpleTypeSchema | None = None

    def __str__(self) -> str:
        if self.var_type is None:
            return f'({TermConnective.LAMBDA}{self.var}.{self.sub})'

        return f'({TermConnective.LAMBDA}{self.var}:{self.var_type}.{self.sub})'


class UntypedAbstractionSchema(MixedAbstractionSchema):
    sub: 'UntypedTermSchema'
    var_type: None


class TypedAbstractionSchema(MixedAbstractionSchema):
    sub: 'TypedTermSchema'
    var_type: SimpleTypeSchema


MixedTermSchema = Constant | VariablePlaceholder | TermPlaceholder | MixedApplicationSchema | MixedAbstractionSchema
UntypedTermSchema = Constant | VariablePlaceholder | TermPlaceholder | UntypedApplicationSchema | UntypedAbstractionSchema
TypedTermSchema = Constant | VariablePlaceholder | TermPlaceholder | TypedApplicationSchema | TypedAbstractionSchema
