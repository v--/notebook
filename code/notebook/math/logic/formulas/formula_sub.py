from dataclasses import dataclass

from ..terms import TermSubstitutionSpec
from .formulas import Formula


@dataclass(frozen=True)
class FormulaSubstitutionSpec:
    formula: Formula
    sub: TermSubstitutionSpec | None = None

    def __str__(self) -> str:
        if self.sub:
            return f'{self.formula}{self.sub}'

        return str(self.formula)
