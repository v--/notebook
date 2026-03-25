from ..exceptions import NotebookMathError


class NumericMathError(NotebookMathError):
    pass


class InvalidArgumentError(NumericMathError, ValueError):
    pass
