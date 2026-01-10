from ..sequents import Sequent, SequentSchema
from .base import AtomicLogicSchemaInstantiation
from .context_application import instantiate_context_schema


def instantiate_sequent_schema(schema: SequentSchema, instantiation: AtomicLogicSchemaInstantiation) -> Sequent:
    return Sequent(
        instantiate_context_schema(schema.left, instantiation),
        instantiate_context_schema(schema.right, instantiation)
    )
