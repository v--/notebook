from ..assertions import TypeAssertion, TypeAssertionSchema
from .base import LambdaSchemaInstantiation, merge_instantiations
from .term_application import instantiate_term_schema
from .term_inference import infer_instantiation_from_term
from .type_application import instantiate_type_schema
from .type_inference import infer_instantiation_from_type


def instantiate_assertion_schema(schema: TypeAssertionSchema, instantiation: LambdaSchemaInstantiation) -> TypeAssertion:
    term = instantiate_term_schema(schema.term, instantiation)
    type_ = instantiate_type_schema(schema.type, instantiation)
    return TypeAssertion(term, type_)


def infer_instantiation_from_assertion(schema: TypeAssertionSchema, assertion: TypeAssertion) -> LambdaSchemaInstantiation:
    return merge_instantiations(
        infer_instantiation_from_term(schema.term, assertion.term),
        infer_instantiation_from_type(schema.type, assertion.type)
    )
