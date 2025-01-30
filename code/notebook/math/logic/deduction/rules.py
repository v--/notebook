from ....support.inference.rules import InferenceRule, InferenceRulePremise, InferenceRuleSystem
from ..formulas import ExtendedFormulaSchema


class NaturalDeductionPremise(InferenceRulePremise[ExtendedFormulaSchema]):
    pass


class NaturalDeductionRule(InferenceRule[ExtendedFormulaSchema, NaturalDeductionPremise]):
    pass


class NaturalDeductionSystem(InferenceRuleSystem[NaturalDeductionRule]):
    pass
