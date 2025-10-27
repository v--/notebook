from dataclasses import dataclass

from ..terms import EigenvariableSchemaSubstitutionSpec, TermSchemaSubstitutionSpec
from .schemas import FormulaSchema


@dataclass(frozen=True)
class FormulaSchemaSubstitutionSpec:
    formula: FormulaSchema
    sub: TermSchemaSubstitutionSpec | EigenvariableSchemaSubstitutionSpec | None = None

    def __str__(self) -> str:
        if self.sub:
            return f'{self.formula}[{self.sub}]'

        return str(self.formula)
