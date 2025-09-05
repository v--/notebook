from ...support.inference import InferenceRule, InferenceRulePremise
from ...support.inference.system import InferenceRuleSystem
from .assertions import TypeAssertionSchema, VariableTypeAssertionSchema


class TypingRulePremise(InferenceRulePremise[TypeAssertionSchema, VariableTypeAssertionSchema]):
    pass


class TypingRule(InferenceRule[TypeAssertionSchema, TypingRulePremise]):
    pass


class ExplicitTypeSystem(InferenceRuleSystem[TypingRule]):
    pass

