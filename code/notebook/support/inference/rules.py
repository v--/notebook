from collections.abc import Sequence
from dataclasses import dataclass

from .alphabet import InferenceRuleConnective


@dataclass(frozen=True)
class InferenceRulePremise[MainT, DischargeT]:
    main: MainT
    discharge: DischargeT | None = None

    def __str__(self) -> str:
        if self.discharge is None:
            return str(self.main)

        return f'[{self.discharge}] {self.main}'


@dataclass(frozen=True)
class InferenceRule[ConclusionT, PremiseT]:
    name: str
    premises: Sequence[PremiseT]
    conclusion: ConclusionT

    def without_name(self) -> str:
        if len(self.premises) > 0:
            premise_str = ', '.join(map(str, self.premises))
            return f'{premise_str} {InferenceRuleConnective.SEQUENT} {self.conclusion}'

        return f'{InferenceRuleConnective.SEQUENT} {self.conclusion}'

    def __str__(self) -> str:
        return f'({self.name}) {self.without_name()}'

    def __hash__(self) -> int:
        return hash((self.name, tuple(self.premises), self.conclusion))
