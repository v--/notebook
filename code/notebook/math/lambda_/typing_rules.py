from collections.abc import Collection

from ...support.inference.rules import InferenceRule, InferenceRulePremise, InferenceRuleSystem
from .assertions import TypeAssertionSchema, TypeAssertionSchemaTyped, TypeAssertionSchemaUntyped


class TypingRulePremise[SchemaT: TypeAssertionSchema](InferenceRulePremise[SchemaT]):
    pass


class TypingRulePremiseUntyped(TypingRulePremise[TypeAssertionSchemaUntyped]):
    pass


class TypingRulePremiseTyped(TypingRulePremise[TypeAssertionSchemaTyped]):
    pass


class TypingRule[SchemaT: TypeAssertionSchema, PremiseT: TypingRulePremise](InferenceRule[SchemaT, PremiseT]):
    pass


class TypingRuleUntyped(TypingRule[TypeAssertionSchemaUntyped, TypingRulePremiseUntyped]):
    pass


class TypingRuleTyped(TypingRule[TypeAssertionSchemaTyped, TypingRulePremiseTyped]):
    pass


class GradualTypingSystem[RuleT: TypingRule](InferenceRuleSystem[RuleT]):
    pass


class ImplicitTypingSystem(GradualTypingSystem[TypingRuleUntyped]):
    rules: Collection[TypingRuleUntyped]


class ExplicitTypingSystem(GradualTypingSystem[TypingRuleTyped]):
    rules: Collection[TypingRuleTyped]
