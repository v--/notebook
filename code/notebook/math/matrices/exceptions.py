from ...exceptions import NotebookCodeError


class MatrixError(NotebookCodeError):
    pass


class MatrixIndexError(MatrixError, IndexError):
    pass


class MatrixValueError(MatrixError, ValueError):
    pass
