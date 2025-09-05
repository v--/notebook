from ....support.inference import InferenceRule, InferenceRulePremise, InferenceRuleSystem
from ..formulas import FormulaSchema


class NaturalDeductionPremise(InferenceRulePremise[FormulaSchema, FormulaSchema]):
    pass


class NaturalDeductionRule(InferenceRule[FormulaSchema, NaturalDeductionPremise]):
    pass


class NaturalDeductionSystem(InferenceRuleSystem[NaturalDeductionRule]):
    pass
