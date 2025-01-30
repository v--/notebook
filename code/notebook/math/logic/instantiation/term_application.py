from dataclasses import dataclass
from typing import override

from ....support.schemas import SchemaInstantiationError
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
from .base import FormalLogicSchemaInstantiation


@dataclass(frozen=True)
class InstantiationApplicationVisitor(TermSchemaVisitor[Term]):
    instantiation: FormalLogicSchemaInstantiation

    @override
    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> Variable:
        if schema not in self.instantiation.variable_mapping:
            raise SchemaInstantiationError(f'No specification of how to instantiate the variable placeholder {schema}')

        return self.instantiation.variable_mapping[schema]

    @override
    def visit_term_placeholder(self, schema: TermPlaceholder) -> Term:
        if schema not in self.instantiation.term_mapping:
            raise SchemaInstantiationError(f'No specification of how to instantiate the term placeholder {schema}')

        return self.instantiation.term_mapping[schema]

    @override
    def visit_function(self, schema: FunctionTermSchema) -> FunctionTerm:
        return FunctionTerm(schema.name, [self.visit(arg) for arg in schema.arguments])


def instantiate_term_schema(schema: TermSchema, instantiation: FormalLogicSchemaInstantiation) -> Term:
    return InstantiationApplicationVisitor(instantiation).visit(schema)
