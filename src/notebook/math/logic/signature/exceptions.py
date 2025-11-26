from ..exceptions import FormalLogicError


class FormalLogicSignatureError(FormalLogicError):
    pass


class MissingSignatureSymbolError(FormalLogicError):
    pass


class SignatureMorphismError(FormalLogicError):
    pass
