from collections.abc import Collection
from dataclasses import dataclass

from ....parsing.identifiers import LatinIdentifier, new_latin_identifier
from ....support.unicode import to_superscript
from ..formulas import Formula, FormulaWithSubstitution
from ..substitution import evaluate_substitution


@dataclass(frozen=True)
class Marker:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


def new_marker(context: Collection[Marker]) -> Marker:
    return Marker(new_latin_identifier({var.identifier for var in context}))


@dataclass(frozen=True)
class MarkedFormula:
    formula: Formula
    marker: Marker

    def __str__(self) -> str:
        return f'[{self.formula}]{to_superscript(str(self.marker))}'


@dataclass(frozen=True)
class MarkedFormulaWithSubstitution:
    payload: FormulaWithSubstitution
    marker: Marker

    @classmethod
    def wrap(cls, value: MarkedFormula | MarkedFormulaWithSubstitution) -> MarkedFormulaWithSubstitution:
        if isinstance(value, MarkedFormulaWithSubstitution):
            return value

        return cls(FormulaWithSubstitution.wrap(value.formula), value.marker)

    def __str__(self) -> str:
        return f'[{self.payload}]{to_superscript(str(self.marker))}'

    def eval(self) -> MarkedFormula:
        return MarkedFormula(evaluate_substitution(self.payload), self.marker)
