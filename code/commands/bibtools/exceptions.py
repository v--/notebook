from ..common.exceptions import NotebookCommandError


class BibToolsError(NotebookCommandError):
    pass


class BibToolsNetworkError(NotebookCommandError):
    pass


class BibToolsParseError(BibToolsError):
    pass


class BibToolsNotFoundError(BibToolsError):
    pass
