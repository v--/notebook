from dataclasses import dataclass
from typing import TYPE_CHECKING

from notebook.math.logic.substitution import evaluate_substitution
from notebook.parsing.identifiers import LatinIdentifier, new_latin_identifier
from notebook.support.unicode import to_superscript


if TYPE_CHECKING:
    from collections.abc import Collection

    from notebook.math.logic.formulas import Formula, FormulaWithSubstitution


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

    def __str__(self) -> str:
        return f'[{self.payload}]{to_superscript(str(self.marker))}'

    def eval(self) -> MarkedFormula:
        return MarkedFormula(evaluate_substitution(self.payload), self.marker)
