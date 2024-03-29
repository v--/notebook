from typing import NamedTuple

from ..fol.formulas import Formula


class ContextEntry(NamedTuple):
    marker: str
    formula: Formula

    def __str__(self):
        return f'{self.formula}:{self.marker}'
