from typing import TYPE_CHECKING

from notebook.math.logic.sequents import Sequent, SequentSchema

from .context_application import instantiate_context_schema


if TYPE_CHECKING:
    from .base import AtomicLogicSchemaInstantiation


def instantiate_sequent_schema(schema: SequentSchema, instantiation: AtomicLogicSchemaInstantiation) -> Sequent:
    return Sequent(
        instantiate_context_schema(schema.left, instantiation),
        instantiate_context_schema(schema.right, instantiation),
    )
