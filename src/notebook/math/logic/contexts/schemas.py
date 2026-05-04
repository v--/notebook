from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Sequence

    from notebook.math.logic.formulas import FormulaSchema
    from notebook.parsing import GreekIdentifier


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
