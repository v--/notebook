from typing import TYPE_CHECKING

from notebook.math.logic.contexts import LogicalContext, LogicalContextPlaceholder, LogicalContextSchema
from notebook.math.logic.formulas import Formula, FormulaSchema
from notebook.support.coderefs import collector
from notebook.support.schemas import SchemaInstantiationError

from .formula_application import instantiate_formula_schema


if TYPE_CHECKING:
    from collections.abc import Iterable

    from .base import AtomicLogicSchemaInstantiation


def _instantiate_context_schema_payload(schema: LogicalContextSchema, instantiation: AtomicLogicSchemaInstantiation) -> Iterable[Formula]:
    for entry in schema.payload:
        if isinstance(entry, FormulaSchema):
            yield instantiate_formula_schema(entry, instantiation)

        if isinstance(entry, LogicalContextPlaceholder):
            if entry not in instantiation.context_mapping:
                raise SchemaInstantiationError(f'No specification of how to instantiate the context placeholder {entry}')

            yield from instantiation.context_mapping[entry]


@collector.ref('alg:logical_context_instantiation')
def instantiate_context_schema(schema: LogicalContextSchema, instantiation: AtomicLogicSchemaInstantiation) -> LogicalContext:
    return LogicalContext(list(_instantiate_context_schema_payload(schema, instantiation)))
