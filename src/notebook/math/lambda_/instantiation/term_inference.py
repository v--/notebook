from dataclasses import dataclass
from typing import override

from ....support.schemas import SchemaInferenceError
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
from .type_inference import infer_instantiation_from_type


@dataclass(frozen=True)
class InferInstantiationVisitor(TypedTermSchemaVisitor[AtomicLambdaSchemaInstantiation]):
    term: TypedTerm

    @override
    def visit_constant(self, schema: Constant) -> AtomicLambdaSchemaInstantiation:
        if self.term != schema:
            raise SchemaInferenceError(f'Cannot match constant {schema} to {self.term}')

        return AtomicLambdaSchemaInstantiation()

    @override
    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> AtomicLambdaSchemaInstantiation:
        if not isinstance(self.term, Variable):
            raise SchemaInferenceError(f'Cannot match variable placeholder {schema} to {self.term}')

        return AtomicLambdaSchemaInstantiation(variable_mapping={schema: self.term})

    @override
    def visit_term_placeholder(self, schema: TermPlaceholder) -> AtomicLambdaSchemaInstantiation:
        return AtomicLambdaSchemaInstantiation(term_mapping={schema: self.term})

    @override
    def visit_application(self, schema: TypedApplicationSchema) -> AtomicLambdaSchemaInstantiation:
        if not isinstance(self.term, TypedApplication):
            raise SchemaInferenceError(f'Cannot match application schema {schema} to {self.term}')

        left = infer_instantiation_from_term(schema.left, self.term.left)
        right = infer_instantiation_from_term(schema.right, self.term.right)
        return left | right

    @override
    def visit_abstraction(self, schema: TypedAbstractionSchema) -> AtomicLambdaSchemaInstantiation:
        if not isinstance(self.term, TypedAbstraction):
            raise SchemaInferenceError(f'Cannot match abstraction schema {schema} to {self.term}')

        return AtomicLambdaSchemaInstantiation(variable_mapping={schema.var: self.term.var}) | \
            infer_instantiation_from_type(schema.var_type, self.term.var_type) | \
            infer_instantiation_from_term(schema.body, self.term.body)


# This is alg:lambda_term_schema_inference in the monograph
def infer_instantiation_from_term(schema: TypedTermSchema, term: TypedTerm) -> AtomicLambdaSchemaInstantiation:
    return InferInstantiationVisitor(term).visit(schema)


def is_term_schema_instance(schema: TypedTermSchema, term: TypedTerm) -> bool:
    try:
        infer_instantiation_from_term(schema, term)
    except SchemaInferenceError:
        return False
    else:
        return True
