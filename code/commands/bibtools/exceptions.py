from ..common.exceptions import NotebookCommandError


class BibToolsError(NotebookCommandError):
    pass


class BibToolsNotFoundError(BibToolsError):
    pass
