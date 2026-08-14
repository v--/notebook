from notebook.exceptions import NotebookError


class CodingError(NotebookError):
    pass


class EncodingError(CodingError):
    pass


class DecodingError(CodingError):
    pass
