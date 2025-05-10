from enum import Flag, auto

from ...support.inference import InferenceRule, InferenceRulePremise
from .assertions import ExplicitTypeAssertionSchema, ImplicitTypeAssertionSchema, TypeAssertionSchema


class TypingStyle(Flag):
    IMPLICIT = auto()
    EXPLICIT = auto()
    GRADUAL = IMPLICIT | EXPLICIT


class TypingRulePremise[SchemaT: TypeAssertionSchema](InferenceRulePremise[SchemaT]):
    pass


class ImplicitTypingRulePremise(TypingRulePremise[ImplicitTypeAssertionSchema]):
    pass


class ExplicitTypingRulePremise(TypingRulePremise[ExplicitTypeAssertionSchema]):
    pass


class TypingRule[SchemaT: TypeAssertionSchema, PremiseT: TypingRulePremise](InferenceRule[SchemaT, PremiseT]):
    pass


class ImplicitTypingRule(TypingRule[ImplicitTypeAssertionSchema, ImplicitTypingRulePremise]):
    pass


class ExplicitTypingRule(TypingRule[ExplicitTypeAssertionSchema, ExplicitTypingRulePremise]):
    pass
