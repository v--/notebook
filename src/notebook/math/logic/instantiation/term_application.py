from dataclasses import dataclass
from typing import overload, override

from ....support.schemas import SchemaInstantiationError
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
class TermInstantiationApplicationVisitor(TermSchemaVisitor[Term]):
    instantiation: AtomicLogicSchemaInstantiation

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
    def visit_function(self, schema: FunctionApplicationSchema) -> FunctionApplication:
        return FunctionApplication(schema.symbol, [self.visit(arg) for arg in schema.arguments])


@overload
def instantiate_term_schema(schema: VariablePlaceholder, instantiation: AtomicLogicSchemaInstantiation) -> Variable: ...
@overload
def instantiate_term_schema(schema: TermSchema, instantiation: AtomicLogicSchemaInstantiation) -> Term: ...
def instantiate_term_schema(schema: TermSchema, instantiation: AtomicLogicSchemaInstantiation) -> Term:
    return TermInstantiationApplicationVisitor(instantiation).visit(schema)
