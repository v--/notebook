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
class GradualTypeAssertion:
    term: MixedTerm
    type: SimpleType

    def __str__(self) -> str:
        return f'{self.term}: {self.type}'


class ImplicitTypeAssertion(GradualTypeAssertion):
    term: UntypedTerm


class ExplicitTypeAssertion(GradualTypeAssertion):
    term: TypedTerm


class VariableTypeAssertion(GradualTypeAssertion):
    term: Variable
    type: SimpleType


@dataclass(frozen=True)
class GradualTypeAssertionSchema:
    term: MixedTermSchema
    type: SimpleTypeSchema

    def __str__(self) -> str:
        return f'{self.term}: {self.type}'


class ImplicitTypeAssertionSchema(GradualTypeAssertionSchema):
    term: UntypedTermSchema


class ExplicitTypeAssertionSchema(GradualTypeAssertionSchema):
    term: TypedTermSchema


class VariableTypeAssertionSchema(GradualTypeAssertionSchema):
    term: VariablePlaceholder
    type: SimpleTypeSchema
