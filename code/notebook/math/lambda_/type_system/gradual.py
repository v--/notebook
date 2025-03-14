from ....support.inference import InferenceRuleSystem
from ..typing import GradualTypingRule


class GradualTypeSystem[RuleT: GradualTypingRule](InferenceRuleSystem[RuleT]):
    pass

