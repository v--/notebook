from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..terms import TermSubstitutionSpec
    from .formulas import Formula


@dataclass(frozen=True)
class FormulaWithSubstitution:
    formula: Formula
    sub: TermSubstitutionSpec

    def __str__(self) -> str:
        return f'{self.formula}[{self.sub}]'
