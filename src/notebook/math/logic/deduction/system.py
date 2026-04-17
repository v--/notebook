from ....support.inference import InferenceRule, InferenceRuleEntry, InferenceRuleSystem
from ..formulas import FormulaSchema


class NaturalDeductionEntry(InferenceRuleEntry[FormulaSchema]):
    pass


class NaturalDeductionRule(InferenceRule[FormulaSchema, NaturalDeductionEntry]):
    pass


class NaturalDeductionSystem(InferenceRuleSystem[NaturalDeductionRule]):
    pass
