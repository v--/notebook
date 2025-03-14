from enum import Flag, auto

from ...support.inference import InferenceRule, InferenceRulePremise
from .assertions import ExplicitTypeAssertionSchema, GradualTypeAssertionSchema, ImplicitTypeAssertionSchema


class TypingStyle(Flag):
    IMPLICIT = auto()
    EXPLICIT = auto()
    GRADUAL = IMPLICIT | EXPLICIT


class GradualTypingRulePremise[SchemaT: GradualTypeAssertionSchema](InferenceRulePremise[SchemaT]):
    pass


class ImplicitTypingRulePremise(GradualTypingRulePremise[ImplicitTypeAssertionSchema]):
    pass


class ExplicitTypingRulePremise(GradualTypingRulePremise[ExplicitTypeAssertionSchema]):
    pass


class GradualTypingRule[SchemaT: GradualTypeAssertionSchema, PremiseT: GradualTypingRulePremise](InferenceRule[SchemaT, PremiseT]):
    pass


class ImplicitTypingRule(GradualTypingRule[ImplicitTypeAssertionSchema, ImplicitTypingRulePremise]):
    pass


class ExplicitTypingRule(GradualTypingRule[ExplicitTypeAssertionSchema, ExplicitTypingRulePremise]):
    pass
