from collections.abc import Sequence
from typing import NamedTuple

from .schemas import FormulaSchema


class Premise(NamedTuple):
    main: FormulaSchema
    discharge: FormulaSchema | None

    def __str__(self) -> str:
        if self.discharge is None:
            return str(self.main)

        return f'[{self.discharge}] {self.main}'


class Rule(NamedTuple):
    name: str
    premises: Sequence[Premise]
    conclusion: FormulaSchema

    def __str__(self) -> str:
        if len(self.premises) > 0:
            premise_str = ', '.join(map(str, self.premises))
            return f'({self.name}) {premise_str} ⫢ {self.conclusion}'

        return f'({self.name}) ⫢ {self.conclusion}'

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(tuple(self.premises)) ^ hash(self.conclusion)
