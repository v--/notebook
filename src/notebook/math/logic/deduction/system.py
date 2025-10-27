from ....support.inference import InferenceRule, InferenceRulePremise, InferenceRuleSystem
from ..formulas import FormulaSchemaSubstitutionSpec


class NaturalDeductionPremise(InferenceRulePremise[FormulaSchemaSubstitutionSpec, FormulaSchemaSubstitutionSpec]):
    pass


class NaturalDeductionRule(InferenceRule[FormulaSchemaSubstitutionSpec, NaturalDeductionPremise]):
    pass


class NaturalDeductionSystem(InferenceRuleSystem[NaturalDeductionRule]):
    pass
