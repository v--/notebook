from dataclasses import dataclass
from typing import override

from ....support.schemas import SchemaInferenceError
from ..terms import (
    FunctionTerm,
    FunctionTermSchema,
    Term,
    TermPlaceholder,
    TermSchema,
    TermSchemaVisitor,
    Variable,
    VariablePlaceholder,
)
from .base import FormalLogicSchemaInstantiation, merge_instantiations


@dataclass(frozen=True)
class InferInstantiationVisitor(TermSchemaVisitor[FormalLogicSchemaInstantiation]):
    term: Term

    @override
    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> FormalLogicSchemaInstantiation:
        if not isinstance(self.term, Variable):
            raise SchemaInferenceError(f'Cannot match variable placeholder {schema} to {self.term}')

        return FormalLogicSchemaInstantiation(variable_mapping={schema: self.term})

    @override
    def visit_term_placeholder(self, schema: TermPlaceholder) -> FormalLogicSchemaInstantiation:
        return FormalLogicSchemaInstantiation(term_mapping={schema: self.term})

    @override
    def visit_function(self, schema: FunctionTermSchema) -> FormalLogicSchemaInstantiation:
        if not isinstance(self.term, FunctionTerm) or schema.name != self.term.name or len(schema.arguments) != len(self.term.arguments):
            raise SchemaInferenceError(f'Cannot match function term schema {schema} to {self.term}')

        instantiation = FormalLogicSchemaInstantiation()

        for subschema, subterm in zip(schema.arguments, self.term.arguments, strict=True):
            instantiation = merge_instantiations(instantiation, infer_instantiation_from_term(subschema, subterm))

        return instantiation


def infer_instantiation_from_term(schema: TermSchema, term: Term) -> FormalLogicSchemaInstantiation:
    return InferInstantiationVisitor(term).visit(schema)


def is_term_schema_instance(schema: TermSchema, term: Term) -> bool:
    try:
        infer_instantiation_from_term(schema, term)
    except SchemaInferenceError:
        return False
    else:
        return True
