from collections.abc import Mapping, Sequence
from typing import Any

from ....support.schemas import SchemaInferenceError, iter_mapping_discrepancy
from ..contexts import LogicalContextPlaceholder
from ..formulas import Formula, FormulaPlaceholder
from ..terms import Term, TermPlaceholder, Variable, VariablePlaceholder


class AtomicLogicSchemaInstantiation:
    formula_mapping: Mapping[FormulaPlaceholder, Formula]
    variable_mapping: Mapping[VariablePlaceholder, Variable]
    term_mapping: Mapping[TermPlaceholder, Term]
    context_mapping: Mapping[LogicalContextPlaceholder, Sequence[Formula]]

    def __init__(
        self,
        *,
        formula_mapping: Mapping[FormulaPlaceholder, Formula] | None = None,
        variable_mapping: Mapping[VariablePlaceholder, Variable] | None = None,
        term_mapping: Mapping[TermPlaceholder, Term] | None = None,
        context_mapping: Mapping[LogicalContextPlaceholder, Sequence[Formula]] | None = None,
    ) -> None:
        self.formula_mapping = formula_mapping or {}
        self.variable_mapping = variable_mapping or {}
        self.term_mapping = term_mapping or {}
        self.context_mapping = context_mapping or {}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AtomicLogicSchemaInstantiation):
            return NotImplemented

        return self.variable_mapping == other.variable_mapping and \
            self.term_mapping == other.term_mapping and \
            self.formula_mapping == other.formula_mapping and \
            self.context_mapping == other.context_mapping

    def __or__(self, other: object) -> AtomicLogicSchemaInstantiation:
        if not isinstance(other, AtomicLogicSchemaInstantiation):
            return NotImplemented

        schema: Any
        a: Any
        b: Any

        for schema, (a, b) in iter_mapping_discrepancy(self.variable_mapping, other.variable_mapping):
            raise SchemaInferenceError(f'Cannot instantiate variable placeholder {schema} to both {a} and {b}')

        for schema, (a, b) in iter_mapping_discrepancy(self.term_mapping, other.term_mapping):
            raise SchemaInferenceError(f'Cannot instantiate term placeholder {schema} to both {a} and {b}')

        for schema, (a, b) in iter_mapping_discrepancy(self.formula_mapping, other.formula_mapping):
            raise SchemaInferenceError(f'Cannot instantiate type placeholder {schema} to both {a} and {b}')

        for schema, (a, b) in iter_mapping_discrepancy(self.context_mapping, other.context_mapping):
            raise SchemaInferenceError(f'Cannot instantiate logical context placeholder {schema} to both {a} and {b}')

        return AtomicLogicSchemaInstantiation(
            variable_mapping={**self.variable_mapping, **other.variable_mapping},
            term_mapping={**self.term_mapping, **other.term_mapping},
            formula_mapping={**self.formula_mapping, **other.formula_mapping},
            context_mapping={**self.context_mapping, **other.context_mapping}
        )
