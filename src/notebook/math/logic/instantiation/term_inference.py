from dataclasses import dataclass
from typing import override

from ....support.schemas import SchemaInferenceError
from ..terms import (
    FunctionApplication,
    FunctionApplicationSchema,
    Term,
    TermPlaceholder,
    TermSchema,
    TermSchemaVisitor,
    Variable,
    VariablePlaceholder,
)
from .base import AtomicLogicSchemaInstantiation


@dataclass(frozen=True)
class InferInstantiationVisitor(TermSchemaVisitor[AtomicLogicSchemaInstantiation]):
    term: Term

    @override
    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> AtomicLogicSchemaInstantiation:
        if not isinstance(self.term, Variable):
            raise SchemaInferenceError(f'Cannot match variable placeholder {schema} to {self.term}')

        return AtomicLogicSchemaInstantiation(variable_mapping={schema: self.term})

    @override
    def visit_term_placeholder(self, schema: TermPlaceholder) -> AtomicLogicSchemaInstantiation:
        return AtomicLogicSchemaInstantiation(term_mapping={schema: self.term})

    @override
    def visit_function(self, schema: FunctionApplicationSchema) -> AtomicLogicSchemaInstantiation:
        if not isinstance(self.term, FunctionApplication) or schema.symbol != self.term.symbol or len(schema.arguments) != len(self.term.arguments):
            raise SchemaInferenceError(f'Cannot match function term schema {schema} to {self.term}')

        instantiation = AtomicLogicSchemaInstantiation()

        for subschema, subterm in zip(schema.arguments, self.term.arguments, strict=True):
            instantiation |= infer_instantiation_from_term(subschema, subterm)

        return instantiation


def infer_instantiation_from_term(schema: TermSchema, term: Term) -> AtomicLogicSchemaInstantiation:
    return InferInstantiationVisitor(term).visit(schema)


def is_term_schema_instance(schema: TermSchema, term: Term) -> bool:
    try:
        infer_instantiation_from_term(schema, term)
    except SchemaInferenceError:
        return False
    else:
        return True
