from ..exceptions import NotebookCommandError


class BibToolsError(NotebookCommandError):
    pass


class BibToolsNetworkError(BibToolsError):
    pass


class BibToolsParsingError(BibToolsError):
    pass


class BibToolsNotFoundError(BibToolsError):
    pass
