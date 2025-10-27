from dataclasses import dataclass

from ..terms import TermSubstitutionSpec
from .formulas import Formula


@dataclass(frozen=True)
class FormulaWithSubstitution:
    formula: Formula
    sub: TermSubstitutionSpec | None = None

    def __str__(self) -> str:
        if self.sub and not self.sub.is_noop():
            return f'{self.formula}[{self.sub}]'

        return str(self.formula)
