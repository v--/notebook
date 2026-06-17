from dataclasses import dataclass

lazy from notebook.math.logic.terms import TermSubstitutionSpec

lazy from .formulas import Formula


@dataclass(frozen=True)
class FormulaWithSubstitution:
    formula: Formula
    sub: TermSubstitutionSpec

    def __str__(self) -> str:
        return f'{self.formula}[{self.sub}]'
