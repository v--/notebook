from dataclasses import dataclass
from typing import overload, override

from ....support.schemas import SchemaInstantiationError
from ..terms import (
    Constant,
    TermPlaceholder,
    TypedAbstraction,
    TypedAbstractionSchema,
    TypedApplication,
    TypedApplicationSchema,
    TypedTerm,
    TypedTermSchema,
    TypedTermSchemaVisitor,
    Variable,
    VariablePlaceholder,
)
from .base import AtomicLambdaSchemaInstantiation
from .type_application import instantiate_type_schema


@dataclass(frozen=True)
class InstantiationApplicationVisitor(TypedTermSchemaVisitor[TypedTerm]):
    instantiation: AtomicLambdaSchemaInstantiation

    @override
    def visit_constant(self, schema: Constant) -> Constant:
        return schema

    @override
    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> Variable:
        if schema not in self.instantiation.variable_mapping:
            raise SchemaInstantiationError(f'No specification of how to instantiate the variable placeholder {schema}')

        return self.instantiation.variable_mapping[schema]

    @override
    def visit_term_placeholder(self, schema: TermPlaceholder) -> TypedTerm:
        if schema not in self.instantiation.term_mapping:
            raise SchemaInstantiationError(f'No specification of how to instantiate the term placeholder {schema}')

        return self.instantiation.term_mapping[schema]

    @override
    def visit_application(self, schema: TypedApplicationSchema) -> TypedApplication:
        return TypedApplication(self.visit(schema.left), self.visit(schema.right))

    @override
    def visit_abstraction(self, schema: TypedAbstractionSchema) -> TypedAbstraction:
        return TypedAbstraction(
            self.visit_variable_placeholder(schema.var),
            instantiate_type_schema(schema.var_type, self.instantiation),
            self.visit(schema.body)
        )


@overload
def instantiate_term_schema(schema: VariablePlaceholder, instantiation: AtomicLambdaSchemaInstantiation) -> Variable: ...
@overload
def instantiate_term_schema(schema: TypedTermSchema, instantiation: AtomicLambdaSchemaInstantiation) -> TypedTerm: ...
def instantiate_term_schema(schema: TypedTermSchema, instantiation: AtomicLambdaSchemaInstantiation) -> TypedTerm:
    return InstantiationApplicationVisitor(instantiation).visit(schema)
