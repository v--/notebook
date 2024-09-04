class NotebookCodeException(Exception):  # noqa: N818
    pass


class NotebookCodeError(NotebookCodeException):
    pass


class UnreachableException(NotebookCodeException):
    pass
