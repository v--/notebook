from typing import TYPE_CHECKING

from notebook.math.lambda_.assertions import TypeAssertion, TypeAssertionSchema
from notebook.support.coderefs import collector

from .term_application import instantiate_term_schema
from .term_inference import infer_instantiation_from_term
from .type_application import instantiate_type_schema
from .type_inference import infer_instantiation_from_type


if TYPE_CHECKING:
    from .base import AtomicLambdaSchemaInstantiation


@collector.ref('alg:type_assertion_schema_instantiation')
def instantiate_assertion_schema(schema: TypeAssertionSchema, instantiation: AtomicLambdaSchemaInstantiation) -> TypeAssertion:
    term = instantiate_term_schema(schema.term, instantiation)
    type_ = instantiate_type_schema(schema.type, instantiation)
    return TypeAssertion(term, type_)


@collector.ref('alg:type_assertion_schema_inference')
def infer_instantiation_from_assertion(schema: TypeAssertionSchema, assertion: TypeAssertion) -> AtomicLambdaSchemaInstantiation:
    return infer_instantiation_from_term(schema.term, assertion.term) | \
        infer_instantiation_from_type(schema.type, assertion.type)
