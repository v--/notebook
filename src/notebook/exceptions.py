class NotebookException(Exception):
    pass


class NotebookError(NotebookException):
    pass


class UnreachableException(NotebookException):
    pass
