from collections.abc import Collection, Sequence
from typing import NamedTuple

from ...parsing.tokens import TokenEnum
from .exceptions import InferenceRuleError


class InferenceRuleConnective(TokenEnum):
    sequent = '⫢'


class InferenceRulePremise[EntryT](NamedTuple):
    main: EntryT
    discharge: EntryT | None

    def __str__(self) -> str:
        if self.discharge is None:
            return str(self.main)

        return f'[{self.discharge}] {self.main}'


class InferenceRule[ConclusionT, PremiseT](NamedTuple):
    name: str
    premises: Sequence[PremiseT]
    conclusion: ConclusionT

    def __str__(self) -> str:
        if len(self.premises) > 0:
            premise_str = ', '.join(map(str, self.premises))
            return f'({self.name}) {premise_str} {InferenceRuleConnective.sequent} {self.conclusion}'

        return f'({self.name}) {InferenceRuleConnective.sequent} {self.conclusion}'

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(tuple(self.premises)) ^ hash(self.conclusion)


class InferenceRuleSystem[RuleT: InferenceRule]:
    rules: Collection[RuleT]

    def __init__(self, rules: Collection[RuleT]) -> None:
        self.rules = rules

    def __getitem__(self, rule_name: str) -> RuleT:
        # We don't enforce the rule names to be distinct, but we hope they are when this method is used
        try:
            return next(rule for rule in self.rules if rule.name == rule_name)
        except StopIteration:
            raise InferenceRuleError(f'Unknown rule {rule_name}') from None
