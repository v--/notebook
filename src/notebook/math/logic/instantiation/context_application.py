from collections.abc import Iterable

from ....support.schemas import SchemaInstantiationError
from ..contexts import LogicalContext, LogicalContextPlaceholder, LogicalContextSchema
from ..formulas import Formula, FormulaSchema
from .base import AtomicLogicSchemaInstantiation
from .formula_application import instantiate_formula_schema


def _instantiate_context_schema_payload(schema: LogicalContextSchema, instantiation: AtomicLogicSchemaInstantiation) -> Iterable[Formula]:
    for entry in schema.payload:
        if isinstance(entry, FormulaSchema):
            yield instantiate_formula_schema(entry, instantiation)

        if isinstance(entry, LogicalContextPlaceholder):
            if entry not in instantiation.context_mapping:
                raise SchemaInstantiationError(f'No specification of how to instantiate the context placeholder {entry}')

            yield from instantiation.context_mapping[entry]


# This is alg:logical_context_instantiation in the monograph
def instantiate_context_schema(schema: LogicalContextSchema, instantiation: AtomicLogicSchemaInstantiation) -> LogicalContext:
    return LogicalContext(list(_instantiate_context_schema_payload(schema, instantiation)))
