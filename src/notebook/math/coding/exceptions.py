from notebook.math.exceptions import NotebookMathError


class CodingError(NotebookMathError):
    pass


class EncodingError(CodingError):
    pass


class DecodingError(CodingError):
    pass
