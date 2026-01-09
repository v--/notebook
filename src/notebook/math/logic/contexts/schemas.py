from collections.abc import Sequence
from dataclasses import dataclass

from ....parsing import GreekIdentifier
from ..formulas import FormulaSchema


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
