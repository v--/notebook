from collections.abc import Collection
from typing import NamedTuple

from ....parsing.identifiers import LatinIdentifier, new_latin_identifier
from ..formulas import Formula


class Marker(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


def new_marker(context: Collection[Marker]) -> Marker:
    return Marker(new_latin_identifier({var.identifier for var in context}))


class MarkedFormula(NamedTuple):
    formula: Formula
    marker: Marker

