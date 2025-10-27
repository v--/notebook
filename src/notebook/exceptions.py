class NotebookException(Exception):  # noqa: N818
    pass


class NotebookError(NotebookException):
    pass


class UnreachableException(NotebookException):
    pass
