from ....support.inference import InferenceRule, InferenceRuleEntry, InferenceRuleSystem
from ..formulas import FormulaSchemaWithSubstitution


class NaturalDeductionEntry(InferenceRuleEntry[FormulaSchemaWithSubstitution, FormulaSchemaWithSubstitution]):
    pass


class NaturalDeductionRule(InferenceRule[NaturalDeductionEntry]):
    pass


class NaturalDeductionSystem(InferenceRuleSystem[NaturalDeductionRule]):
    pass
