from collections.abc import Mapping, Sequence

from ....support.schemas import SchemaInferenceError, iter_mapping_discrepancy
from ..contexts import LogicalContextPlaceholder
from ..formulas import Formula, FormulaPlaceholder
from ..terms import Term, TermPlaceholder, Variable, VariablePlaceholder
from .base import AtomicLogicSchemaInstantiation


class AtomicLogicalContextSchemaInstantiation(AtomicLogicSchemaInstantiation):
    context_mapping: Mapping[LogicalContextPlaceholder, Sequence[Formula]]

    def __init__(
        self,
        *,
        formula_mapping: Mapping[FormulaPlaceholder, Formula] | None = None,
        variable_mapping: Mapping[VariablePlaceholder, Variable] | None = None,
        term_mapping: Mapping[TermPlaceholder, Term] | None = None,
        context_mapping: Mapping[LogicalContextPlaceholder, Sequence[Formula]] | None = None,
    ) -> None:
        super().__init__(
            formula_mapping=formula_mapping,
            variable_mapping=variable_mapping,
            term_mapping=term_mapping
        )

        self.context_mapping = context_mapping or {}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AtomicLogicalContextSchemaInstantiation):
            return NotImplemented

        return super().__eq__(other) and self.context_mapping == other.context_mapping

    def __or__(self, other: object) -> AtomicLogicalContextSchemaInstantiation:
        if not isinstance(other, AtomicLogicalContextSchemaInstantiation):
            return NotImplemented

        s = super().__or__(other)

        for schema, (a, b) in iter_mapping_discrepancy(self.context_mapping, other.context_mapping):
            raise SchemaInferenceError(f'Cannot instantiate context placeholder {schema} to both {a} and {b}')

        return AtomicLogicalContextSchemaInstantiation(
            term_mapping=s.term_mapping,
            formula_mapping=s.formula_mapping,
            variable_mapping=s.variable_mapping,
            context_mapping={**self.context_mapping, **other.context_mapping}
        )
