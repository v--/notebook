from ....support.inference import InferenceRuleSystem
from ..typing import TypingRule


class GradualTypeSystem[RuleT: TypingRule](InferenceRuleSystem[RuleT]):
    pass

