from ...exceptions import NotebookCodeError


class NotebookUnicodeError(NotebookCodeError, UnicodeError):
    pass


class UnrecognizedCharacterError(NotebookUnicodeError):
    pass
