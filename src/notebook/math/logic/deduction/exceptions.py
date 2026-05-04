from notebook.math.logic.exceptions import FormalLogicError
from notebook.support.inference import UnknownInferenceRuleError


class NaturalDeductionError(FormalLogicError):
    pass


class RuleApplicationError(FormalLogicError):
    pass


class UnknownNaturalDeductionRuleError(UnknownInferenceRuleError):
    pass
