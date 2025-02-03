from dataclasses import dataclass
from typing import overload, override

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
    TypedAbstraction,
    TypedApplication,
    TypedApplicationSchema,
    TypedTerm,
    TypedTermSchema,
    UntypedAbstraction,
    UntypedApplication,
    UntypedApplicationSchema,
    UntypedTerm,
    UntypedTermSchema,
    Variable,
    VariablePlaceholder,
)
from .base import LambdaSchemaInstantiation, TypedLambdaSchemaInstantiation, UntypedLambdaSchemaInstantiation
from .type_application import instantiate_type_schema


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
        match (schema, self.instantiation):
            case (UntypedApplicationSchema(), UntypedLambdaSchemaInstantiation()):
                return UntypedApplication(self.visit(schema.a), self.visit(schema.b))

            case (TypedApplicationSchema(), TypedLambdaSchemaInstantiation()):
                return TypedApplication(self.visit(schema.a), self.visit(schema.b))

            case _:
                return Application(self.visit(schema.a), self.visit(schema.b))

    @override
    def visit_abstraction(self, schema: AbstractionSchema) -> Abstraction:
        match (schema, self.instantiation):
            case (UntypedApplicationSchema(), UntypedLambdaSchemaInstantiation()):
                return UntypedAbstraction(self.visit_variable_placeholder(schema.var), self.visit(schema.sub))

            case (TypedApplicationSchema(), TypedLambdaSchemaInstantiation()):
                return TypedAbstraction(
                    self.visit_variable_placeholder(schema.var),
                    self.visit(schema.sub),
                    instantiate_type_schema(schema.var_type, self.instantiation)
                )

            case _:
                return Abstraction(
                    self.visit_variable_placeholder(schema.var),
                    self.visit(schema.sub),
                    instantiate_type_schema(schema.var_type, self.instantiation) if schema.var_type else None
                )


@overload
def instantiate_term_schema(schema: UntypedTermSchema, instantiation: UntypedLambdaSchemaInstantiation) -> UntypedTerm: ...
@overload
def instantiate_term_schema(schema: TypedTermSchema, instantiation: TypedLambdaSchemaInstantiation) -> TypedTerm: ...
@overload
def instantiate_term_schema(schema: TermSchema, instantiation: LambdaSchemaInstantiation) -> Term: ...
def instantiate_term_schema(schema: TermSchema, instantiation: LambdaSchemaInstantiation) -> Term:
    return InstantiationApplicationVisitor(instantiation).visit(schema)
