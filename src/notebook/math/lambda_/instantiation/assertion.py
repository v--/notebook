from typing import TYPE_CHECKING

from ..assertions import TypeAssertion, TypeAssertionSchema
from .term_application import instantiate_term_schema
from .term_inference import infer_instantiation_from_term
from .type_application import instantiate_type_schema
from .type_inference import infer_instantiation_from_type


if TYPE_CHECKING:
    from .base import AtomicLambdaSchemaInstantiation


# This is alg:type_assertion_schema_instantiation in the monograph
def instantiate_assertion_schema(schema: TypeAssertionSchema, instantiation: AtomicLambdaSchemaInstantiation) -> TypeAssertion:
    term = instantiate_term_schema(schema.term, instantiation)
    type_ = instantiate_type_schema(schema.type, instantiation)
    return TypeAssertion(term, type_)


# This is alg:type_assertion_schema_inference in the monograph
def infer_instantiation_from_assertion(schema: TypeAssertionSchema, assertion: TypeAssertion) -> AtomicLambdaSchemaInstantiation:
    return infer_instantiation_from_term(schema.term, assertion.term) | \
        infer_instantiation_from_type(schema.type, assertion.type)
