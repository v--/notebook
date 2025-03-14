from collections.abc import Mapping
from typing import Any

from ....support.schemas import SchemaInferenceError, iter_mapping_discrepancy
from ..terms import (
    MixedTerm,
    TermPlaceholder,
    TypedTerm,
    UntypedTerm,
    Variable,
    VariablePlaceholder,
)
from ..types import (
    SimpleType,
    TypePlaceholder,
)


class LambdaSchemaInstantiation:
    variable_mapping: Mapping[VariablePlaceholder, Variable]
    term_mapping: Mapping[TermPlaceholder, MixedTerm]
    type_mapping: Mapping[TypePlaceholder, SimpleType]

    def __init__(
        self,
        *,
        variable_mapping: Mapping[VariablePlaceholder, Variable] | None = None,
        term_mapping: Mapping[TermPlaceholder, MixedTerm] | None = None,
        type_mapping: Mapping[TypePlaceholder, SimpleType] | None = None
    ) -> None:
        self.variable_mapping = variable_mapping or {}
        self.term_mapping = term_mapping or {}
        self.type_mapping = type_mapping or {}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LambdaSchemaInstantiation):
            return NotImplemented

        return self.variable_mapping == other.variable_mapping and \
            self.term_mapping == other.term_mapping and \
            self.type_mapping == other.type_mapping



def is_instantiation_implicitly_typed(instantiation: LambdaSchemaInstantiation) -> bool:
    return all(isinstance(term, UntypedTerm) for term in instantiation.term_mapping.values())


def is_instantiation_explicitly_typed(instantiation: LambdaSchemaInstantiation) -> bool:
    return all(isinstance(term, TypedTerm) for term in instantiation.term_mapping.values())


def merge_instantiations(left: LambdaSchemaInstantiation, right: LambdaSchemaInstantiation) -> LambdaSchemaInstantiation:
    schema: Any
    a: Any
    b: Any

    for schema, (a, b) in iter_mapping_discrepancy(left.variable_mapping, right.variable_mapping):
        raise SchemaInferenceError(f'Cannot instantiate variable placeholder {schema} to both {a} and {b}')

    for schema, (a, b) in iter_mapping_discrepancy(left.term_mapping, right.term_mapping):
        raise SchemaInferenceError(f'Cannot instantiate term placeholder {schema} to both {a} and {b}')

    for schema, (a, b) in iter_mapping_discrepancy(left.type_mapping, right.type_mapping):
        raise SchemaInferenceError(f'Cannot instantiate type placeholder {schema} to both {a} and {b}')

    return LambdaSchemaInstantiation(
        variable_mapping={**left.variable_mapping, **right.variable_mapping},
        term_mapping={**left.term_mapping, **right.term_mapping},
        type_mapping={**left.type_mapping, **right.type_mapping}
    )
