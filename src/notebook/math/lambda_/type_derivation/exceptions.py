from notebook.math.lambda_.exceptions import LambdaCalculusError
from notebook.support.inference import UnknownInferenceRuleError


class TypeDerivationError(LambdaCalculusError):
    pass


class TypeDerivationRuleError(TypeDerivationError):
    pass


class TypeInferenceError(LambdaCalculusError):
    pass


class UnknownDerivationRuleError(UnknownInferenceRuleError):
    pass
