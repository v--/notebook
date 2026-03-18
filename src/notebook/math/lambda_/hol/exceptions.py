from ..exceptions import LambdaCalculusError
from ..signature.exceptions import LambdaSignatureError


class HolError(LambdaCalculusError):
    pass


class HolSignatureError(LambdaSignatureError):
    pass


class NonQuantifiableTypeError(LambdaSignatureError):
    pass
