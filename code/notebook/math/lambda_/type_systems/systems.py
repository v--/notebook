from collections.abc import Collection

from ....support.inference.rules import InferenceRuleSystem
from ..typing import ExplicitTypingRule, GradualTypingRule, ImplicitTypingRule


class GradualTypingSystem[RuleT: GradualTypingRule](InferenceRuleSystem[RuleT]):
    pass


class ImplicitTypingSystem(GradualTypingSystem[ImplicitTypingRule]):
    rules: Collection[ImplicitTypingRule]


class ExplicitTypingSystem(GradualTypingSystem[ExplicitTypingRule]):
    rules: Collection[ExplicitTypingRule]
