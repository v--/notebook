from notebook.math.logic.formulas import FormulaSchema
from notebook.support.inference import InferenceRule, InferenceRuleEntry, InferenceRuleSystem


class NaturalDeductionEntry(InferenceRuleEntry[FormulaSchema]):
    pass


class NaturalDeductionRule(InferenceRule[FormulaSchema, NaturalDeductionEntry]):
    pass


class NaturalDeductionSystem(InferenceRuleSystem[NaturalDeductionRule]):
    pass
