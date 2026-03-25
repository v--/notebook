from ..exceptions import NotebookMathError


class MatrixError(NotebookMathError):
    pass


class MatrixIndexError(MatrixError, IndexError):
    pass


class MatrixValueError(MatrixError, ValueError):
    pass


class IncompatibleMatrixError(MatrixError, ValueError):
    pass
