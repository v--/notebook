from notebook.exceptions import NotebookError, NotebookException


class NotebookMathException(NotebookException):
    pass


class NotebookMathError(NotebookMathException, NotebookError):
    pass
