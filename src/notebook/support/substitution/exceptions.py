from notebook.support.exceptions import NotebookSupportError


class SubstitutionError(NotebookSupportError):
    pass


class UnspecifiedReplacementError(SubstitutionError):
    pass
