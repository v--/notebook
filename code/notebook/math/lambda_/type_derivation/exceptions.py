from ....support.inference import UnknownInferenceRuleError
from ..exceptions import LambdaCalculusError


class TypeDerivationError(LambdaCalculusError):
    pass


class TypeDerivationRuleError(TypeDerivationError):
    pass


class TypeInferenceError(LambdaCalculusError):
    pass


class UnknownDerivationRuleError(UnknownInferenceRuleError):
    pass
