from dataclasses import dataclass

from .exceptions import NaturalDeductionError
from .rules import Rule


@dataclass
class NaturalDeductionSystem:
    rules: frozenset[Rule]

    def __getitem__(self, rule_name: str) -> Rule:
        # We don't enforce the rule names to be distinct, but we hope they are when this method is used
        try:
            return next(rule for rule in self.rules if rule.name == rule_name)
        except StopIteration:
            raise NaturalDeductionError(f'Unknown rule {rule_name}') from None
