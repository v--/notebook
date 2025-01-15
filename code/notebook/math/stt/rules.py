from collections.abc import Sequence
from typing import NamedTuple

from .alphabet import RuleConnective
from .assertions import TypeAssertionSchema


class TypeRulePremise(NamedTuple):
    main: TypeAssertionSchema
    discharge: TypeAssertionSchema | None

    def __str__(self) -> str:
        if self.discharge is None:
            return str(self.main)

        return f'[{self.discharge}] {self.main}'


class TypeRule(NamedTuple):
    name: str
    premises: Sequence[TypeRulePremise]
    conclusion: TypeAssertionSchema

    def __str__(self) -> str:
        if len(self.premises) > 0:
            premise_str = ', '.join(map(str, self.premises))
            return f'({self.name}) {premise_str} {RuleConnective.sequent} {self.conclusion}'

        return f'({self.name}) {RuleConnective.sequent} {self.conclusion}'

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(tuple(self.premises)) ^ hash(self.conclusion)
