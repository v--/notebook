from ..exceptions import NotebookMathError


class FormalLogicError(NotebookMathError):
    pass


class FormalLogicSignatureError(FormalLogicError):
    pass


class SignatureTranslationError(FormalLogicError):
    pass
