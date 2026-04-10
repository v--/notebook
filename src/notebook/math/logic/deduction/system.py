from ....support.inference import InferenceRule, InferenceRuleEntry, InferenceRuleSystem
from ..formulas import FormulaSchema


class NaturalDeductionEntry(InferenceRuleEntry[FormulaSchema, FormulaSchema]):
    pass


class NaturalDeductionRule(InferenceRule[NaturalDeductionEntry]):
    pass


class NaturalDeductionSystem(InferenceRuleSystem[NaturalDeductionRule]):
    pass
