from ...exceptions import NotebookCodeError


class LambdaCalculusError(NotebookCodeError):
    pass


class LambdaSignatureError(LambdaCalculusError):
    pass
