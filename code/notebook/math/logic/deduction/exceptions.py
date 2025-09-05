from ....support.inference import UnknownInferenceRuleError
from ..exceptions import FormalLogicError


class NaturalDeductionError(FormalLogicError):
    pass


class RuleApplicationError(FormalLogicError):
    pass


class UnknownNaturalDeductionRuleError(UnknownInferenceRuleError):
    pass
