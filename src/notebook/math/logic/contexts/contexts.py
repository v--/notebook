from dataclasses import dataclass
lazy from collections.abc import Sequence

lazy from notebook.math.logic.formulas import Formula


@dataclass(frozen=True)
class LogicalContext:
    payload: Sequence[Formula]

    def __str__(self) -> str:
        return ', '.join(str(formula) for formula in self.payload)

    def __repr__(self) -> str:
        return f"parse_context('{self}')"
