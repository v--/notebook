from dataclasses import dataclass

from ..terms import EigenSchemaSubstitutionSpec, TermSchemaSubstitutionSpec
from .schemas import FormulaSchema


@dataclass(frozen=True)
class FormulaSchemaWithSubstitution:
    formula: FormulaSchema
    sub: TermSchemaSubstitutionSpec | None = None

    def __str__(self) -> str:
        if self.sub:
            return f'{self.formula}[{self.sub}]'

        return str(self.formula)


class FormulaSchemaWithEigenvariable(FormulaSchemaWithSubstitution):
    sub: EigenSchemaSubstitutionSpec
