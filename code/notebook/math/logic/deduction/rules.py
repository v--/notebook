from ....support.inference import InferenceRule, InferenceRulePremise
from ..formulas import ExtendedFormulaSchema


class NaturalDeductionPremise(InferenceRulePremise[ExtendedFormulaSchema]):
    pass


class NaturalDeductionRule(InferenceRule[ExtendedFormulaSchema, NaturalDeductionPremise]):
    pass
