from ..exceptions import LambdaCalculusError


class HolError(LambdaCalculusError):
    pass


class HolSignatureError(HolError):
    pass


class LambdaInterpretationError(HolError):
    pass


class MissingInterpretationError(LambdaInterpretationError):
    pass
