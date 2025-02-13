from ...exceptions import NotebookCodeError


class SubstitutionError(NotebookCodeError):
    pass


class UnspecifiedReplacementError(SubstitutionError):
    pass
