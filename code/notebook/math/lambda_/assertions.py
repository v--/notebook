from typing import NamedTuple

from .alphabet import TypeAssertionConnective
from .terms import (
    Term,
    TermSchema,
    TypedTerm,
    TypedTermSchema,
    UntypedTerm,
    UntypedTermSchema,
    Variable,
    VariablePlaceholder,
)
from .types import SimpleType, SimpleTypeSchema


class TypeAssertion(NamedTuple):
    term: Term
    type: SimpleType

    def __str__(self) -> str:
        return f'{self.term}{TypeAssertionConnective.colon} {self.type}'


class TypeAssertionTyped(TypeAssertion):
    term: TypedTerm


class TypeAssertionUntyped(TypeAssertion):
    term: UntypedTerm


class VariableTypeAssertion(TypeAssertion):
    term: Variable
    type: SimpleType


class TypeAssertionSchema(NamedTuple):
    term: TermSchema
    type: SimpleTypeSchema

    def __str__(self) -> str:
        return f'{self.term}{TypeAssertionConnective.colon} {self.type}'


class TypeAssertionSchemaTyped(TypeAssertionSchema):
    term: TypedTermSchema


class TypeAssertionSchemaUntyped(TypeAssertionSchema):
    term: UntypedTermSchema


class VariableTypeAssertionSchema(TypeAssertionSchema):
    term: VariablePlaceholder
    type: SimpleTypeSchema
