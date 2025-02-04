from dataclasses import dataclass

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


@dataclass(frozen=True)
class GradualTypeAssertion:
    term: Term
    type: SimpleType

    def __str__(self) -> str:
        return f'{self.term}{TypeAssertionConnective.colon} {self.type}'


class ImplicitTypeAssertion(GradualTypeAssertion):
    term: UntypedTerm


class ExplicitTypeAssertion(GradualTypeAssertion):
    term: TypedTerm


class VariableTypeAssertion(GradualTypeAssertion):
    term: Variable
    type: SimpleType


@dataclass(frozen=True)
class GradualTypeAssertionSchema:
    term: TermSchema
    type: SimpleTypeSchema

    def __str__(self) -> str:
        return f'{self.term}{TypeAssertionConnective.colon} {self.type}'


class ImplicitTypeAssertionSchema(GradualTypeAssertionSchema):
    term: UntypedTermSchema


class ExplicitTypeAssertionSchema(GradualTypeAssertionSchema):
    term: TypedTermSchema


class VariableTypeAssertionSchema(GradualTypeAssertionSchema):
    term: VariablePlaceholder
    type: SimpleTypeSchema
