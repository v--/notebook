from dataclasses import dataclass

from .terms import (
    TypedTerm,
    TypedTermSchema,
    Variable,
    VariablePlaceholder,
)
from .types import SimpleType, SimpleTypeSchema


@dataclass(frozen=True)
class TypeAssertion:
    term: TypedTerm
    type: SimpleType

    def __str__(self) -> str:
        return f'{self.term}: {self.type}'

    def __iter__(self) -> tuple[TypedTerm, SimpleType]:
        return (self.term, self.type)


class VariableTypeAssertion(TypeAssertion):
    term: Variable


@dataclass(frozen=True)
class TypeAssertionSchema:
    term: TypedTermSchema
    type: SimpleTypeSchema

    def __str__(self) -> str:
        return f'{self.term}: {self.type}'

    def __iter__(self) -> tuple[TypedTermSchema, SimpleTypeSchema]:
        return (self.term, self.type)


class VariableTypeAssertionSchema(TypeAssertionSchema):
    term: VariablePlaceholder
