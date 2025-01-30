from ...support.inference.rules import InferenceRule, InferenceRulePremise, InferenceRuleSystem
from .assertions import TypeAssertionSchema


class TypingRulePremise(InferenceRulePremise[TypeAssertionSchema]):
    pass


class TypingRule(InferenceRule[TypeAssertionSchema, TypingRulePremise]):
    pass


class TypingSystem(InferenceRuleSystem[TypingRule]):
    pass
