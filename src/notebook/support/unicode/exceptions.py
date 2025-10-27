from ..exceptions import NotebookSupportError


class NotebookUnicodeError(NotebookSupportError, UnicodeError):
    pass


class UnrecognizedCharacterError(NotebookUnicodeError):
    pass
