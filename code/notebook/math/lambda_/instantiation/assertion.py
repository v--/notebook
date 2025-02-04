from typing import overload

from ..assertions import (
    ExplicitTypeAssertion,
    ExplicitTypeAssertionSchema,
    GradualTypeAssertion,
    GradualTypeAssertionSchema,
    ImplicitTypeAssertion,
    ImplicitTypeAssertionSchema,
)
from .base import LambdaSchemaInstantiation, merge_instantiations
from .term_application import instantiate_term_schema
from .term_inference import infer_instantiation_from_term
from .type_application import instantiate_type_schema
from .type_inference import infer_instantiation_from_type


@overload
def instantiate_assertion_schema(schema: ImplicitTypeAssertionSchema, instantiation: LambdaSchemaInstantiation) -> ImplicitTypeAssertion: ...
@overload
def instantiate_assertion_schema(schema: ExplicitTypeAssertionSchema, instantiation: LambdaSchemaInstantiation) -> ExplicitTypeAssertion: ...
@overload
def instantiate_assertion_schema(schema: GradualTypeAssertionSchema, instantiation: LambdaSchemaInstantiation) -> GradualTypeAssertion: ...
def instantiate_assertion_schema(schema: GradualTypeAssertionSchema, instantiation: LambdaSchemaInstantiation) -> GradualTypeAssertion:
    term = instantiate_term_schema(schema.term, instantiation)
    type_ = instantiate_type_schema(schema.type, instantiation)

    match GradualTypeAssertion:
        case ImplicitTypeAssertion():
            return ImplicitTypeAssertion(term, type_)

        case ExplicitTypeAssertion():
            return ExplicitTypeAssertion(term, type_)

        case _:
            return GradualTypeAssertion(term, type_)


def infer_instantiation_from_assertion(schema: GradualTypeAssertionSchema, assertion: GradualTypeAssertion) -> LambdaSchemaInstantiation:
    return merge_instantiations(
        infer_instantiation_from_term(schema.term, assertion.term),
        infer_instantiation_from_type(schema.type, assertion.type)
    )
