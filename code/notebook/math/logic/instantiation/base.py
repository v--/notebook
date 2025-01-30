from collections.abc import Mapping
from typing import Any

from ....support.schemas import SchemaInferenceError, iter_mapping_discrepancy
from ..formulas import Formula, FormulaPlaceholder
from ..terms import Term, TermPlaceholder, Variable, VariablePlaceholder


class FormalLogicSchemaInstantiation:
    formula_mapping: Mapping[FormulaPlaceholder, Formula]
    variable_mapping: Mapping[VariablePlaceholder, Variable]
    term_mapping: Mapping[TermPlaceholder, Term]

    def __init__(
        self,
        *,
        formula_mapping: Mapping[FormulaPlaceholder, Formula] | None = None,
        variable_mapping: Mapping[VariablePlaceholder, Variable] | None = None,
        term_mapping: Mapping[TermPlaceholder, Term] | None = None
    ) -> None:
        self.formula_mapping = formula_mapping or {}
        self.variable_mapping = variable_mapping or {}
        self.term_mapping = term_mapping or {}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FormalLogicSchemaInstantiation):
            return NotImplemented

        return self.variable_mapping == other.variable_mapping and \
            self.term_mapping == other.term_mapping and \
            self.formula_mapping == other.formula_mapping


EMPTY_INSTANTIATION = FormalLogicSchemaInstantiation()


def merge_instantiations(left: FormalLogicSchemaInstantiation, right: FormalLogicSchemaInstantiation) -> FormalLogicSchemaInstantiation:
    schema: Any
    a: Any
    b: Any

    for schema, (a, b) in iter_mapping_discrepancy(left.variable_mapping, right.variable_mapping):
        raise SchemaInferenceError(f'Cannot instantiate variable placeholder {schema} to both {a} and {b}')

    for schema, (a, b) in iter_mapping_discrepancy(left.term_mapping, right.term_mapping):
        raise SchemaInferenceError(f'Cannot instantiate term placeholder {schema} to both {a} and {b}')

    for schema, (a, b) in iter_mapping_discrepancy(left.formula_mapping, right.formula_mapping):
        raise SchemaInferenceError(f'Cannot instantiate type placeholder {schema} to both {a} and {b}')

    return FormalLogicSchemaInstantiation(
        variable_mapping={**left.variable_mapping, **right.variable_mapping},
        term_mapping={**left.term_mapping, **right.term_mapping},
        formula_mapping={**left.formula_mapping, **right.formula_mapping}
    )
