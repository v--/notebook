from dataclasses import dataclass

from .terms import (
    MixedTerm,
    MixedTermSchema,
    TypedTerm,
    TypedTermSchema,
    UntypedTerm,
    UntypedTermSchema,
    Variable,
    VariablePlaceholder,
)
from .types import SimpleType, SimpleTypeSchema


@dataclass(frozen=True)
class TypeAssertion:
    term: MixedTerm
    type: SimpleType

    def __str__(self) -> str:
        return f'{self.term}: {self.type}'


class ImplicitTypeAssertion(TypeAssertion):
    term: UntypedTerm


class ExplicitTypeAssertion(TypeAssertion):
    term: TypedTerm


class VariableTypeAssertion(TypeAssertion):
    term: Variable
    type: SimpleType


@dataclass(frozen=True)
class TypeAssertionSchema:
    term: MixedTermSchema
    type: SimpleTypeSchema

    def __str__(self) -> str:
        return f'{self.term}: {self.type}'


class ImplicitTypeAssertionSchema(TypeAssertionSchema):
    term: UntypedTermSchema


class ExplicitTypeAssertionSchema(TypeAssertionSchema):
    term: TypedTermSchema


class VariableTypeAssertionSchema(TypeAssertionSchema):
    term: VariablePlaceholder
    type: SimpleTypeSchema
