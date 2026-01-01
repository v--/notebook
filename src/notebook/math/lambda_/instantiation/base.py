from collections.abc import Mapping
from typing import Any

from ....support.schemas import SchemaInferenceError, iter_mapping_discrepancy
from ..terms import (
    TermPlaceholder,
    TypedTerm,
    Variable,
    VariablePlaceholder,
)
from ..types import (
    SimpleType,
    TypePlaceholder,
)


class AtomicLambdaSchemaInstantiation:
    variable_mapping: Mapping[VariablePlaceholder, Variable]
    term_mapping: Mapping[TermPlaceholder, TypedTerm]
    type_mapping: Mapping[TypePlaceholder, SimpleType]

    def __init__(
        self,
        *,
        variable_mapping: Mapping[VariablePlaceholder, Variable] | None = None,
        term_mapping: Mapping[TermPlaceholder, TypedTerm] | None = None,
        type_mapping: Mapping[TypePlaceholder, SimpleType] | None = None
    ) -> None:
        self.variable_mapping = variable_mapping or {}
        self.term_mapping = term_mapping or {}
        self.type_mapping = type_mapping or {}

    def __hash__(self) -> int:
        return hash((self.variable_mapping, self.term_mapping, self.type_mapping))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AtomicLambdaSchemaInstantiation):
            return NotImplemented

        return self.variable_mapping == other.variable_mapping and \
            self.term_mapping == other.term_mapping and \
            self.type_mapping == other.type_mapping

    def __or__(self, other: AtomicLambdaSchemaInstantiation) -> AtomicLambdaSchemaInstantiation:
        schema: Any
        a: Any
        b: Any

        for schema, (a, b) in iter_mapping_discrepancy(self.variable_mapping, other.variable_mapping):
            raise SchemaInferenceError(f'Cannot instantiate variable placeholder {schema} to both {a} and {b}')

        for schema, (a, b) in iter_mapping_discrepancy(self.term_mapping, other.term_mapping):
            raise SchemaInferenceError(f'Cannot instantiate term placeholder {schema} to both {a} and {b}')

        for schema, (a, b) in iter_mapping_discrepancy(self.type_mapping, other.type_mapping):
            raise SchemaInferenceError(f'Cannot instantiate type placeholder {schema} to both {a} and {b}')

        return AtomicLambdaSchemaInstantiation(
            variable_mapping={**self.variable_mapping, **other.variable_mapping},
            term_mapping={**self.term_mapping, **other.term_mapping},
            type_mapping={**self.type_mapping, **other.type_mapping}
        )
