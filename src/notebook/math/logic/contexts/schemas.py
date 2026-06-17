from dataclasses import dataclass
lazy from collections.abc import Sequence

lazy from notebook.math.logic.formulas import FormulaSchema
lazy from notebook.parsing import GreekIdentifier


@dataclass(frozen=True)
class LogicalContextPlaceholder:
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)

    def __repr__(self) -> str:
        return f"parse_context_schema('{self}')"


@dataclass(frozen=True)
class LogicalContextSchema:
    payload: Sequence[LogicalContextPlaceholder | FormulaSchema]

    def __str__(self) -> str:
        return ', '.join(str(schema) for schema in self.payload)

    def __repr__(self) -> str:
        return f"parse_context_schema('{self}')"
