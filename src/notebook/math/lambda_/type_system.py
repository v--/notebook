from notebook.support.inference import InferenceRule, InferenceRuleEntry
from notebook.support.inference.system import InferenceRuleSystem

from .assertions import TypeAssertionSchema, VariableTypeAssertionSchema


class TypingRuleEntry(InferenceRuleEntry[TypeAssertionSchema, VariableTypeAssertionSchema]):
    pass


class TypingRule(InferenceRule[TypingRuleEntry]):
    pass


class ExplicitTypeSystem(InferenceRuleSystem[TypingRule]):
    pass
