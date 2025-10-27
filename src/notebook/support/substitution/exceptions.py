from ..exceptions import NotebookSupportError


class SubstitutionError(NotebookSupportError):
    pass


class UnspecifiedReplacementError(SubstitutionError):
    pass
