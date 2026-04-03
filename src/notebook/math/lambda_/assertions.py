from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .terms import TypedTerm, TypedTermSchema, Variable, VariablePlaceholder
    from .types import SimpleType, SimpleTypeSchema


@dataclass(frozen=True)
class TypeAssertion:
    term: TypedTerm
    type: SimpleType

    def __str__(self) -> str:
        return f'{self.term}: {self.type}'

    def __repr__(self) -> str:
        return f"parse_type_assertion('{self}')"

    def unpack(self) -> tuple[TypedTerm, SimpleType]:
        return (self.term, self.type)


class VariableTypeAssertion(TypeAssertion):
    term: Variable

    def __repr__(self) -> str:
        return f"parse_variable_assertion('{self}')"


@dataclass(frozen=True)
class TypeAssertionSchema:
    term: TypedTermSchema
    type: SimpleTypeSchema

    def __str__(self) -> str:
        return f'{self.term}: {self.type}'

    def __repr__(self) -> str:
        return f"parse_type_assertion_schema('{self}')"

    def unpack(self) -> tuple[TypedTermSchema, SimpleTypeSchema]:
        return (self.term, self.type)


class VariableTypeAssertionSchema(TypeAssertionSchema):
    term: VariablePlaceholder
