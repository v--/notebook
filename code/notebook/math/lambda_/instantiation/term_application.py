from dataclasses import dataclass
from typing import override

from ....support.schemas import SchemaInstantiationError
from ..terms import (
    Abstraction,
    AbstractionSchema,
    Application,
    ApplicationSchema,
    Constant,
    Term,
    TermPlaceholder,
    TermSchema,
    TermSchemaVisitor,
    Variable,
    VariablePlaceholder,
)
from .base import LambdaSchemaInstantiation


@dataclass(frozen=True)
class InstantiationApplicationVisitor(TermSchemaVisitor[Term]):
    instantiation: LambdaSchemaInstantiation

    @override
    def visit_constant(self, schema: Constant) -> Constant:
        return schema

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
    def visit_application(self, schema: ApplicationSchema) -> Application:
        return Application(self.visit(schema.a), self.visit(schema.b))

    @override
    def visit_abstraction(self, schema: AbstractionSchema) -> Abstraction:
        return Abstraction(self.visit_variable_placeholder(schema.var), self.visit(schema.sub))


def instantiate_term_schema(schema: TermSchema, instantiation: LambdaSchemaInstantiation) -> Term:
    return InstantiationApplicationVisitor(instantiation).visit(schema)
