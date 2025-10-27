from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass

from .rules import InferenceRule


@dataclass(frozen=True)
class InferenceRuleSystem[RuleT: InferenceRule](Mapping[str, RuleT]):
    rules: Sequence[RuleT]

    def __getitem__(self, key: str) -> RuleT:
        for rule in self.rules:
            if rule.name == key:
                return rule

        raise KeyError

    def __contains__(self, key: object) -> bool:
        return any(rule.name == key for rule in self.rules)

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self) -> Iterator[str]:
        for rule in self.rules:
            yield rule.name
