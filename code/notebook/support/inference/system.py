from collections.abc import Iterator, Mapping
from dataclasses import dataclass

from .rules import InferenceRule


@dataclass(frozen=True)
class InferenceRuleSystem[RuleT: InferenceRule](Mapping[str, RuleT]):
    rules: Mapping[str, RuleT]

    def __getitem__(self, key: str) -> RuleT:
        return self.rules[key]

    def __contains__(self, key: object) -> bool:
        return key in self.rules

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self) -> Iterator[str]:
        return iter(self.rules)
