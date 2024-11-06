from ..exceptions import LinAlgError


class MatrixIndexError(LinAlgError, IndexError):
    pass


class MatrixValueError(LinAlgError, ValueError):
    pass
