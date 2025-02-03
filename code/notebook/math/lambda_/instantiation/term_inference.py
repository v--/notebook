from dataclasses import dataclass
from typing import override

from ....support.schemas import SchemaInferenceError
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
from .base import (
    LambdaSchemaInstantiation,
    merge_instantiations,
)
from .type_inference import infer_instantiation_from_type


@dataclass(frozen=True)
class InferInstantiationVisitor(TermSchemaVisitor[LambdaSchemaInstantiation]):
    term: Term

    @override
    def visit_constant(self, schema: Constant) -> LambdaSchemaInstantiation:
        if self.term != schema:
            raise SchemaInferenceError(f'Cannot match constant {schema} to {self.term}')

        return LambdaSchemaInstantiation()

    @override
    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> LambdaSchemaInstantiation:
        if not isinstance(self.term, Variable):
            raise SchemaInferenceError(f'Cannot match variable placeholder {schema} to {self.term}')

        return LambdaSchemaInstantiation(variable_mapping={schema: self.term})

    @override
    def visit_term_placeholder(self, schema: TermPlaceholder) -> LambdaSchemaInstantiation:
        return LambdaSchemaInstantiation(term_mapping={schema: self.term})

    @override
    def visit_application(self, schema: ApplicationSchema) -> LambdaSchemaInstantiation:
        if not isinstance(self.term, Application):
            raise SchemaInferenceError(f'Cannot match application schema {schema} to {self.term}')

        a = infer_instantiation_from_term(schema.a, self.term.a)
        b = infer_instantiation_from_term(schema.b, self.term.b)
        return merge_instantiations(a, b)

    @override
    def visit_abstraction(self, schema: AbstractionSchema) -> LambdaSchemaInstantiation:
        if not isinstance(self.term, Abstraction):
            raise SchemaInferenceError(f'Cannot match abstraction schema {schema} to {self.term}')

        instantiation = LambdaSchemaInstantiation(variable_mapping={schema.var: self.term.var})

        if schema.var_type is not None:
            if self.term.var_type is None:
                raise SchemaInferenceError(f'The schema {schema} has a type annotation on its abstractor, but the term {self.term} does not')

            instantiation = merge_instantiations(
                instantiation,
                infer_instantiation_from_type(schema.var_type, self.term.var_type)
            )

        return merge_instantiations(
            instantiation,
            infer_instantiation_from_term(schema.sub, self.term.sub)
        )


def infer_instantiation_from_term(schema: TermSchema, term: Term) -> LambdaSchemaInstantiation:
    return InferInstantiationVisitor(term).visit(schema)


def is_term_schema_instance(schema: TermSchema, term: Term) -> bool:
    try:
        infer_instantiation_from_term(schema, term)
    except SchemaInferenceError:
        return False
    else:
        return True
