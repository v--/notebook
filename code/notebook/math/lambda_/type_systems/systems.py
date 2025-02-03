from collections.abc import Collection

from ....support.inference.rules import InferenceRuleSystem
from ..typing_rules import TypingRule, TypingRuleTyped, TypingRuleUntyped


class GradualTypingSystem[RuleT: TypingRule](InferenceRuleSystem[RuleT]):
    pass


class ImplicitTypingSystem(GradualTypingSystem[TypingRuleUntyped]):
    rules: Collection[TypingRuleUntyped]


class ExplicitTypingSystem(GradualTypingSystem[TypingRuleTyped]):
    rules: Collection[TypingRuleTyped]
