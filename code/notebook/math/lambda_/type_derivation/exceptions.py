from ..exceptions import LambdaCalculusError


class TypeDerivationError(LambdaCalculusError):
    pass


class TypeDerivationRuleError(TypeDerivationError):
    pass


class UnknownDerivationRuleError(TypeDerivationRuleError):
    pass


class TypeInferenceError(LambdaCalculusError):
    pass
