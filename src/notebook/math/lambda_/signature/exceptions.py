from ..exceptions import LambdaCalculusError


class LambdaSignatureError(LambdaCalculusError):
    pass


class MissingSignatureSymbolError(LambdaSignatureError):
    pass


class SignatureMorphismError(LambdaSignatureError):
    pass
